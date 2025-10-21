"""
Chatbot service using Google Gemini AI for financial advice and analysis
Agent-based with tool calling for smart database access
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Callable
from sqlalchemy.orm import Session
from sqlalchemy import and_
import json

try:
    import google.genai as genai
except ImportError:
    genai = None

from .models import Transaction
from .config import settings


class FinancialChatbot:
    """AI-powered financial chatbot using Google Gemini"""
    
    def __init__(self):
        """Initialize the chatbot with Gemini AI"""
        if genai is None:
            raise ImportError("google-genai package is required. Install with: pip install google-genai")
        
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required in environment variables")
        
        # Configure Gemini AI
        self.client = genai.Client(api_key=settings.gemini_api_key)
        
        # Database session and user_id for agent tools
        self.db = None
        self.user_id = None
        
        # Conversation history per user
        self.conversation_history = {}
        
        # Define available tools for the agent
        self.tools = self._define_tools()
        
        # System prompt for conversational financial advisor agent
        self.system_prompt = """
        Bạn là Fin - một AI Financial Advisor thân thiện, thông minh và biết lắng nghe.
        
        TÍNH CÁCH & PHONG CÁCH:
        - Thân thiện như một người bạn, không cứng nhắc
        - Biết lắng nghe và trò chuyện tự nhiên
        - Có thể bàn luận về nhiều chủ đề, không chỉ tài chính
        - Khuyến khích người dùng chia sẻ
        - Sử dụng emoji khi phù hợp (😊, 💰, 📊, 👍, ✨)
        
        KHẢ NĂNG TRÒ CHUYỆN:
        1. Trò chuyện bình thường:
           - Trả lời các câu hỏi thường ngày
           - Chat về cuộc sống, sở thích, kế hoạch
           - Động viên, khuyến khích người dùng
           - Tạo không khí thoải mái
        
        2. Tư vấn tài chính:
           - Lắng nghe hoàn cảnh, mục tiêu của người dùng
           - Đưa ra lời khuyên phù hợp với từng người
           - Giải thích dễ hiểu, không quá kỹ thuật
           - Động viên khi cần thiết
        
        3. Phân tích dữ liệu:
           - Dùng tools khi cần số liệu cụ thể
           - Giải thích kết quả một cách dễ hiểu
           - Đưa ra góc nhìn tích cực và xây dựng
        
        QUY TẮC SỬ DỤNG TOOLS:
        
        KHÔNG dùng tools cho:
        - Chào hỏi, hỏi thăm
        - Trò chuyện thường ngày
        - Câu hỏi chung về tài chính
        - Giải thích khái niệm
        - Hỏi về cảm xúc, ý kiến cá nhân
        
        CHỈ dùng tools khi:
        - "Tôi chi bao nhiêu cho..."
        - "Phân tích chi tiêu của tôi"
        - "Thu nhập/chi tiêu của tôi"
        - "Top danh mục chi tiêu của tôi"
        
        CÁCH TRẢ LỜI:
        1. Ngắn gọn và tự nhiên (như chat với bạn bè)
        2. Sử dụng emoji cho thân thiện (😊 💰 📊 👍 ✨)
        3. KHÔNG dùng ** để in đậm
        4. KHÔNG dùng --- để phân cách
        5. Đặt câu hỏi ngược lại để tạo hội thoại
        6. Động viên và tích cực
        
        VÍ DỤ TRẢ LỜI TỐT:
        
        Q: "Hôm nay trời đẹp quá"
        A: "Đúng vậy! Trời đẹp thế này đi dạo hay shopping đều tuyệt nhỉ 😊 Bạn có kế hoạch gì không?"
        
        Q: "Mình đang buồn"
        A: "Mình hiểu bạn đang cảm thấy không vui. Có chuyện gì xảy ra không? Nếu liên quan đến tài chính, mình có thể giúp bạn phân tích và tìm giải pháp đấy 💪"
        
        Q: "Làm sao tiết kiệm được?"
        A: "Tiết kiệm không khó như bạn nghĩ đâu! 3 tips đơn giản:
        - Ghi chép chi tiêu hàng ngày
        - Cắt giảm những thứ không cần thiết
        - Đặt mục tiêu tiết kiệm cụ thể
        
        Bạn muốn mình phân tích chi tiêu của bạn không? 📊"
        
        Q: "Thủ đô Việt Nam ở đâu?"
        A: "Thủ đô Việt Nam là Hà Nội đấy! Bạn đang có kế hoạch đi Hà Nội à? 🏛️"
        
        Q: "Phân tích chi tiêu của tôi"
        A: [Dùng tools → Lấy dữ liệu → Phân tích]
        "Mình đã xem qua chi tiêu của bạn rồi nhé! Đây là những gì mình thấy:
        [Phân tích ngắn gọn]
        Bạn muốn mình gợi ý cách cải thiện không? 😊"
        
        QUAN TRỌNG:
        - Luôn thân thiện và tích cực
        - Trò chuyện tự nhiên như người bạn
        - Đặt câu hỏi để duy trì cuộc trò chuyện
        - Động viên và khuyến khích
        - Chỉ phân tích tài chính khi được yêu cầu
        
        Hãy là một người bạn tốt, không chỉ là chatbot! 🤗
        """
    
    def _define_tools(self) -> List[Dict[str, Any]]:
        """Define tools available for the agent"""
        return [
            {
                "name": "get_financial_summary",
                "description": "Lấy tóm tắt tài chính của người dùng bao gồm tổng thu nhập, tổng chi tiêu, số dư và số lượng giao dịch trong khoảng thời gian nhất định",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "days": {
                            "type": "integer",
                            "description": "Số ngày muốn xem (mặc định 30 ngày)"
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "get_top_expenses",
                "description": "Lấy top danh mục chi tiêu nhiều nhất của người dùng",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "days": {
                            "type": "integer",
                            "description": "Số ngày muốn xem (mặc định 30 ngày)"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Số lượng danh mục muốn xem (mặc định 5)"
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "get_category_expense",
                "description": "Lấy tổng chi tiêu của một danh mục cụ thể",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category_name": {
                            "type": "string",
                            "description": "Tên danh mục cần xem (ví dụ: 'Ăn uống', 'Di chuyển', 'Mua sắm')"
                        },
                        "days": {
                            "type": "integer",
                            "description": "Số ngày muốn xem (mặc định 30 ngày)"
                        }
                    },
                    "required": ["category_name"]
                }
            },
            {
                "name": "get_spending_analysis",
                "description": "Phân tích mẫu chi tiêu chi tiết và đưa ra nhận xét về tình hình tài chính",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "days": {
                            "type": "integer",
                            "description": "Số ngày muốn phân tích (mặc định 30 ngày)"
                        }
                    },
                    "required": []
                }
            }
        ]
    
    def _execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> str:
        """Execute a tool and return the result"""
        try:
            if tool_name == "get_financial_summary":
                days = parameters.get("days", 30)
                data = self.get_user_financial_data(self.db, self.user_id, days)
                return json.dumps({
                    "total_income": data['total_income'],
                    "total_expense": data['total_expense'],
                    "net_balance": data['net_balance'],
                    "transaction_count": data['transaction_count'],
                    "period": data['period']
                }, ensure_ascii=False)
            
            elif tool_name == "get_top_expenses":
                days = parameters.get("days", 30)
                limit = parameters.get("limit", 5)
                data = self.get_user_financial_data(self.db, self.user_id, days)
                top_categories = data['top_expense_categories'][:limit]
                return json.dumps({
                    "top_expenses": [{"category": cat, "amount": amt} for cat, amt in top_categories]
                }, ensure_ascii=False)
            
            elif tool_name == "get_category_expense":
                category_name = parameters.get("category_name")
                days = parameters.get("days", 30)
                data = self.get_user_financial_data(self.db, self.user_id, days)
                
                # Find category in top expenses
                for cat, amt in data['top_expense_categories']:
                    if category_name.lower() in cat.lower() or cat.lower() in category_name.lower():
                        return json.dumps({
                            "category": cat,
                            "amount": amt,
                            "period": data['period']
                        }, ensure_ascii=False)
                
                return json.dumps({
                    "category": category_name,
                    "amount": 0,
                    "message": "Không tìm thấy chi tiêu cho danh mục này"
                }, ensure_ascii=False)
            
            elif tool_name == "get_spending_analysis":
                days = parameters.get("days", 30)
                data = self.get_user_financial_data(self.db, self.user_id, days)
                analysis = self.analyze_spending_patterns(data)
                recommendations = self.get_budget_recommendations(data)
                return json.dumps({
                    "analysis": analysis,
                    "recommendations": recommendations,
                    "financial_data": {
                        "total_income": data['total_income'],
                        "total_expense": data['total_expense'],
                        "net_balance": data['net_balance']
                    }
                }, ensure_ascii=False)
            
            else:
                return json.dumps({"error": f"Unknown tool: {tool_name}"}, ensure_ascii=False)
                
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    def get_user_financial_data(self, db: Session, user_id: int, days: int = 30) -> Dict[str, Any]:
        """Lấy dữ liệu tài chính của người dùng trong khoảng thời gian nhất định"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        # Lấy tất cả giao dịch trong khoảng thời gian
        transactions = db.query(Transaction).filter(
            and_(
                Transaction.user_id == user_id,
                Transaction.date >= start_date,
                Transaction.date <= end_date,
                Transaction.is_deleted == False
            )
        ).all()
        
        # Tính toán thống kê
        total_income = sum(t.amount for t in transactions if t.type == 'income')
        total_expense = sum(t.amount for t in transactions if t.type == 'expense')
        net_balance = total_income - total_expense
        
        # Phân tích theo danh mục
        category_analysis = {}
        for transaction in transactions:
            if transaction.type == 'expense':
                category_name = transaction.category.name
                if category_name not in category_analysis:
                    category_analysis[category_name] = 0
                category_analysis[category_name] += transaction.amount
        
        # Top 5 danh mục chi tiêu nhiều nhất
        top_expense_categories = sorted(
            category_analysis.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        # Phân tích theo ngày trong tuần
        daily_expenses = {}
        for transaction in transactions:
            if transaction.type == 'expense':
                day_name = transaction.date.strftime('%A')
                if day_name not in daily_expenses:
                    daily_expenses[day_name] = 0
                daily_expenses[day_name] += transaction.amount
        
        return {
            'period': f"{days} ngày gần nhất",
            'total_income': total_income,
            'total_expense': total_expense,
            'net_balance': net_balance,
            'transaction_count': len(transactions),
            'top_expense_categories': top_expense_categories,
            'daily_expenses': daily_expenses,
            'transactions': [
                {
                    'date': t.date.isoformat(),
                    'amount': t.amount,
                    'type': t.type,
                    'description': t.description,
                    'category': t.category.name,
                    'notes': t.notes
                } for t in transactions
            ]
        }
    
    def analyze_spending_patterns(self, financial_data: Dict[str, Any]) -> str:
        """Phân tích mẫu chi tiêu và đưa ra nhận xét"""
        analysis = []
        
        # Phân tích tổng quan
        if financial_data['net_balance'] > 0:
            analysis.append(f"[+] Bạn đang có thặng dư {financial_data['net_balance']:,.0f} VND trong {financial_data['period']}")
        elif financial_data['net_balance'] < 0:
            analysis.append(f"[-] Bạn đang chi tiêu vượt thu nhập {abs(financial_data['net_balance']):,.0f} VND trong {financial_data['period']}")
        else:
            analysis.append(f"[=] Thu chi của bạn đang cân bằng trong {financial_data['period']}")
        
        # Phân tích danh mục chi tiêu
        if financial_data['top_expense_categories']:
            top_category = financial_data['top_expense_categories'][0]
            analysis.append(f"[TOP] Danh mục chi tiêu nhiều nhất: {top_category[0]} ({top_category[1]:,.0f} VND)")
        
        # Phân tích tần suất giao dịch
        avg_daily_transactions = financial_data['transaction_count'] / 30
        if avg_daily_transactions > 5:
            analysis.append("[INFO] Bạn có tần suất giao dịch khá cao, hãy cân nhắc gộp các giao dịch nhỏ")
        elif avg_daily_transactions < 1:
            analysis.append("[INFO] Tần suất giao dịch thấp, có thể bạn đang bỏ sót một số chi tiêu")
        
        return "\n".join(analysis)
    
    def _get_conversation_history(self, user_id: int) -> List[Dict[str, str]]:
        """Lấy lịch sử trò chuyện của user"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        return self.conversation_history[user_id]
    
    def _add_to_history(self, user_id: int, role: str, message: str):
        """Thêm tin nhắn vào lịch sử"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            "role": role,
            "message": message
        })
        
        # Giới hạn lịch sử chỉ giữ 10 tin nhắn gần nhất (5 cặp hỏi-đáp)
        if len(self.conversation_history[user_id]) > 10:
            self.conversation_history[user_id] = self.conversation_history[user_id][-10:]
    
    def _clear_history(self, user_id: int):
        """Xóa lịch sử trò chuyện"""
        if user_id in self.conversation_history:
            self.conversation_history[user_id] = []
    
    def _format_history_for_prompt(self, user_id: int) -> str:
        """Format lịch sử thành chuỗi cho prompt"""
        history = self._get_conversation_history(user_id)
        if not history:
            return ""
        
        formatted = "\n\nLịch sử trò chuyện trước đó:\n"
        for item in history:
            role_name = "User" if item["role"] == "user" else "Fin"
            formatted += f"{role_name}: {item['message']}\n"
        
        return formatted
    
    def _is_simple_greeting(self, message: str) -> bool:
        """Kiểm tra xem có phải câu chào hỏi đơn giản không"""
        simple_patterns = [
            'chào', 'hello', 'hi', 'hey', 'xin chào',
            'chào bạn', 'hế nhô', 'hế lô', 'alo'
        ]
        message_lower = message.lower().strip()
        return any(pattern in message_lower for pattern in simple_patterns) and len(message.split()) <= 3
    
    def _is_finance_related(self, message: str) -> bool:
        """Kiểm tra xem câu hỏi có liên quan đến tài chính không"""
        finance_keywords = [
            'tiền', 'chi', 'thu', 'tiêu', 'tiết kiệm', 'đầu tư',
            'thu nhập', 'chi tiêu', 'ngân sách', 'lương', 'tài chính',
            'quản lý', 'phân tích', 'danh mục', 'giao dịch'
        ]
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in finance_keywords)
    
    def _is_general_question(self, message: str) -> bool:
        """Kiểm tra xem có phải câu hỏi chung không cần dữ liệu"""
        # Nếu không liên quan đến tài chính → câu hỏi chung
        if not self._is_finance_related(message):
            return True
        
        general_keywords = [
            'làm sao', 'làm thế nào', 'cách nào', 'phương pháp',
            'là gì', 'giải thích', 'định nghĩa',
            'lời khuyên chung', 'nên làm gì', 'tôi nên'
        ]
        data_keywords = [
            'chi bao nhiêu', 'thu nhập của tôi', 'phân tích chi tiêu của tôi',
            'top chi tiêu', 'danh mục của tôi', 'số liệu của tôi', 'dữ liệu của tôi',
            'tháng này của tôi', 'tháng trước của tôi'
        ]
        
        message_lower = message.lower()
        has_general = any(keyword in message_lower for keyword in general_keywords)
        has_data = any(keyword in message_lower for keyword in data_keywords)
        
        # Nếu có từ khóa chung và không có từ khóa dữ liệu → câu hỏi chung
        return has_general and not has_data
    
    def _answer_general_question(self, question: str, user_id: int = None) -> str:
        """Trả lời câu hỏi chung không cần dữ liệu - Conversational style with history"""
        
        # Lấy lịch sử nếu có user_id
        history_context = ""
        if user_id:
            history_context = self._format_history_for_prompt(user_id)
        
        prompt = f"""
        Bạn là Fin - một AI thân thiện đang chat với người dùng.
        {history_context}
        
        Tin nhắn hiện tại: {question}
        
        Hãy trả lời:
        1. Thân thiện và tự nhiên như chat với bạn bè
        2. NHỚ lịch sử trò chuyện và đề cập đến nó nếu liên quan
        3. Sử dụng emoji phù hợp (😊 💰 📊 👍 ✨ 💪 🎯)
        4. KHÔNG dùng ** để in đậm
        5. KHÔNG dùng --- để phân cách
        6. Ngắn gọn (2-5 dòng)
        7. Nếu phù hợp, đặt câu hỏi ngược để duy trì hội thoại
        8. Tích cực và động viên
        
        Ví dụ với context:
        - Nếu trước đó nói về đầu tư và giờ hỏi "Có" → "Tuyệt! Để mình gợi ý một số kênh đầu tư phù hợp..."
        - Nếu trước đó nói về chi tiêu và giờ hỏi "Thế nào?" → "À, về chi tiêu bạn hỏi trước đó à?..."
        
        Hãy trả lời tự nhiên, nhớ ngữ cảnh và thân thiện!
        """
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            return f"Xin lỗi, mình gặp chút vấn đề kỹ thuật. Bạn thử hỏi lại được không? 😅"
    
    def generate_financial_advice_with_agent(self, user_question: str, db: Session, user_id: int) -> str:
        """
        Tạo lời khuyên tài chính sử dụng AI Agent với tool calling
        Agent sẽ tự quyết định khi nào cần truy vấn database
        """
        # Set database context for tools
        self.db = db
        self.user_id = user_id
        
        # Quick response for simple greetings
        if self._is_simple_greeting(user_question):
            return "Xin chào! Mình là Fin - trợ lý tài chính của bạn 😊\n\nMình có thể giúp bạn:\n- Chat về bất cứ điều gì\n- Tư vấn tài chính cá nhân\n- Phân tích chi tiêu của bạn\n- Gợi ý cách tiết kiệm thông minh\n\nHôm nay bạn muốn trò chuyện về gì? 💬"
        
        # Direct answer for general questions (no tools needed)
        if self._is_general_question(user_question):
            return self._answer_general_question(user_question, user_id)
        
        # Prepare the prompt for the agent
        full_prompt = f"""
        {self.system_prompt}
        
        Câu hỏi: {user_question}
        
        Quy tắc:
        - Nếu hỏi về số liệu cụ thể → Sử dụng tools
        - Nếu hỏi chung → Trả lời trực tiếp ngắn gọn (3-5 dòng)
        - KHÔNG dùng ** để in đậm
        - Tập trung vào câu hỏi
        """
        
        try:
            # Try to use function calling if supported
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt,
                config={
                    "tools": [{"function_declarations": self.tools}] if self.tools else None,
                    "tool_config": {"function_calling_config": {"mode": "AUTO"}}
                }
            )
            
            # Check if model wants to use tools
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    for part in candidate.content.parts:
                        if hasattr(part, 'function_call'):
                            # Execute the tool
                            function_call = part.function_call
                            tool_result = self._execute_tool(
                                function_call.name,
                                dict(function_call.args)
                            )
                            
                            # Send tool result back to model
                            final_response = self.client.models.generate_content(
                                model="gemini-2.5-flash",
                                contents=[
                                    full_prompt,
                                    {
                                        "role": "model",
                                        "parts": [{"function_call": function_call}]
                                    },
                                    {
                                        "role": "user",
                                        "parts": [{
                                            "function_response": {
                                                "name": function_call.name,
                                                "response": {"result": tool_result}
                                            }
                                        }]
                                    }
                                ]
                            )
                            return final_response.text
            
            # No tool call needed, return direct response
            return response.text
            
        except Exception as e:
            # Fallback: If tool calling fails, use simple approach
            return self._fallback_response(user_question, db, user_id, str(e))
    
    def _fallback_response(self, user_question: str, db: Session, user_id: int, error: str = "") -> str:
        """Fallback response when agent fails"""
        try:
            # Get financial data directly
            financial_data = self.get_user_financial_data(db, user_id, 30)
            
            # Create simple prompt
            data_summary = f"""
            Dữ liệu tài chính trong {financial_data['period']}:
            - Thu nhập: {financial_data['total_income']:,.0f} VND
            - Chi tiêu: {financial_data['total_expense']:,.0f} VND  
            - Số dư: {financial_data['net_balance']:,.0f} VND
            
            Top chi tiêu: {', '.join([f"{cat}: {amt:,.0f}" for cat, amt in financial_data['top_expense_categories'][:3]])}
            """
            
            prompt = f"""
            Bạn là chuyên gia tài chính. Dựa trên dữ liệu sau:
            
            {data_summary}
            
            Câu hỏi: {user_question}
            
            Hãy đưa ra lời khuyên ngắn gọn và hữu ích.
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Xin lỗi, tôi gặp lỗi khi xử lý yêu cầu của bạn: {str(e)}"
    
    def generate_financial_advice(self, financial_data: Dict[str, Any], user_question: str = "") -> str:
        """Legacy method - kept for backward compatibility"""
        data_summary = f"""
        Dữ liệu tài chính trong {financial_data['period']}:
        - Thu nhập: {financial_data['total_income']:,.0f} VND
        - Chi tiêu: {financial_data['total_expense']:,.0f} VND
        - Số dư: {financial_data['net_balance']:,.0f} VND
        
        Top chi tiêu: {', '.join([f"{cat}: {amt:,.0f}" for cat, amt in financial_data['top_expense_categories'][:5]])}
        """
        
        spending_analysis = self.analyze_spending_patterns(financial_data)
        
        full_prompt = f"""
        Bạn là chuyên gia tài chính. Đưa ra lời khuyên dựa trên:
        
        {data_summary}
        
        Phân tích: {spending_analysis}
        
        Câu hỏi: {user_question if user_question else "Lời khuyên tài chính tổng quát"}
        """
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt
            )
            return response.text
        except Exception as e:
            return f"Xin lỗi, tôi gặp lỗi khi xử lý yêu cầu của bạn: {str(e)}"
    
    def get_budget_recommendations(self, financial_data: Dict[str, Any]) -> str:
        """Đưa ra khuyến nghị về ngân sách"""
        if financial_data['total_income'] == 0:
            return "Không có dữ liệu thu nhập để đưa ra khuyến nghị ngân sách."
        
        # Tính tỷ lệ chi tiêu theo thu nhập
        expense_ratio = financial_data['total_expense'] / financial_data['total_income']
        
        recommendations = []
        
        if expense_ratio > 0.9:
            recommendations.append("[WARNING] CẢNH BÁO: Bạn đang chi tiêu hơn 90% thu nhập. Hãy cắt giảm chi tiêu ngay!")
        elif expense_ratio > 0.8:
            recommendations.append("[WARNING] Cảnh báo: Bạn đang chi tiêu hơn 80% thu nhập. Nên tiết kiệm nhiều hơn.")
        elif expense_ratio < 0.5:
            recommendations.append("[GOOD] Tuyệt vời! Bạn đang tiết kiệm hơn 50% thu nhập. Hãy duy trì!")
        else:
            recommendations.append("[OK] Tỷ lệ chi tiêu của bạn đang ở mức hợp lý.")
        
        # Khuyến nghị cụ thể cho từng danh mục
        if financial_data['top_expense_categories']:
            top_category = financial_data['top_expense_categories'][0]
            category_ratio = top_category[1] / financial_data['total_income']
            
            if category_ratio > 0.3:
                recommendations.append(f"[TIP] Gợi ý: Danh mục '{top_category[0]}' chiếm {category_ratio:.1%} thu nhập. Hãy cân nhắc giảm chi tiêu ở đây.")
        
        return "\n".join(recommendations)
    
    def chat_with_user(self, db: Session, user_id: int, message: str, days: int = 30) -> Dict[str, Any]:
        """
        Xử lý tin nhắn từ người dùng và trả về phản hồi
        Sử dụng AI Agent để tự động quyết định có cần truy vấn database
        Lưu lịch sử trò chuyện để nhớ ngữ cảnh
        """
        try:
            # Thêm tin nhắn user vào lịch sử
            self._add_to_history(user_id, "user", message)
            
            # Use agent-based approach with tool calling
            response = self.generate_financial_advice_with_agent(message, db, user_id)
            
            # Thêm phản hồi của bot vào lịch sử
            self._add_to_history(user_id, "bot", response)
            
            # Only get financial summary if question is finance-related
            result = {
                'success': True,
                'response': response,
                'agent_mode': True
            }
            
            # Only include financial summary for finance-related questions
            if self._is_finance_related(message) and not self._is_general_question(message):
                financial_data = self.get_user_financial_data(db, user_id, days)
                result['financial_summary'] = {
                    'total_income': financial_data['total_income'],
                    'total_expense': financial_data['total_expense'],
                    'net_balance': financial_data['net_balance'],
                    'period': financial_data['period']
                }
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Lỗi khi xử lý yêu cầu: {str(e)}",
                'response': "Xin lỗi, tôi gặp lỗi khi xử lý yêu cầu của bạn. Vui lòng thử lại sau."
            }


# Global chatbot instance
chatbot = FinancialChatbot()
