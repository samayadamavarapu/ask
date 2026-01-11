import openai
from transformers import pipeline
import logging
from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class GenerationService:
    def __init__(self):
        self.use_local = False
        # Check if API key is present and valid-looking
        if settings.OPENAI_API_KEY and "your_openai_api_key" not in settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        else:
            self.use_local = True
            logger.info("No valid OpenAI API Key found. Initializing local FLAN-T5 model (this may take a moment to download)...")
            try:
                # Use google/flan-t5-base for a good balance of speed and quality
                self.local_generator = pipeline("text2text-generation", model="google/flan-t5-base")
                logger.info("Local model loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load local model: {e}")
                self.local_generator = None
        
    def generate_response(self, query: str, context: list[str], safety_flag: str) -> str:
        """
        Generates a response based on the query and retrieved context.
        Enforces 'answer only from context'.
        """
        if not context:
            return "I'm sorry, I couldn't find any relevant information in my knowledge base to answer your question."

        context_str = "\n\n".join(context)
        
        # System prompt for OpenAI
        system_prompt = (
            "You are a knowledgeable Yoga and Wellness assistant. "
            "Answer the user's question strictly based on the provided Context below. "
            "If the answer is not in the context, say 'I don't have enough information to answer that.' "
            "Do not hallucinate or provide outside information. "
            "Keep your answer concise, accurate, and friendly."
        )
        
        if safety_flag == "SENSITIVE":
            system_prompt += " The user asked a sensitive question. Be extra careful and purely factual based on context."

        user_prompt = f"Context:\n{context_str}\n\nQuestion: {query}"

        try:
            if self.use_local:
                if not self.local_generator:
                    return "[ERROR] OpenAI Key missing and local model failed to load."
                
                # Prepare prompt for FLAN-T5
                # FLAN-T5 works well with: "Answer the question based on the context: {context} Question: {query}"
                # We need to be mindful of token limits (512 usually for T5)
                # We'll take the most relevant chunk or truncate context
                
                short_context = context[0] if context else ""
                # Rough character limit to stay within ~512 tokens
                if len(short_context) > 1500:
                    short_context = short_context[:1500]
                
                input_text = f"Answer the question based on the context provided. Context: {short_context} Question: {query}"
                
                response = self.local_generator(input_text, max_length=200, do_sample=False)
                return response[0]['generated_text']

            # OpenAI Generation
            response = openai.ChatCompletion.create(
                model=settings.LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3, # Low temperature for factualness
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error generating response: {str(e)}"

_generation_service = None
def get_generation_service() -> GenerationService:
    global _generation_service
    if _generation_service is None:
        _generation_service = GenerationService()
    return _generation_service
