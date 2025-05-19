import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline
import asyncio

class TextGenerator:
    def __init__(self):
        self.model_name = "MODEL_NAME"
        self.generator = None

    async def initialize(self):
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True
        )
        
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map="cuda:0",
            quantization_config=bnb_config,
            torch_dtype=torch.float16
        )
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        self.generator = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=768,
            do_sample=True,
            temperature=0.7,
            top_p=0.95,
            repetition_penalty=1.1
        )

    async def generate_text_async(self, prompt):
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self._generate_text_sync, prompt)
        torch.cuda.empty_cache()

        if isinstance(result, list) and len(result) > 0:
            return result[0]['generated_text']
        return ""

    def _generate_text_sync(self, prompt):
        if not self.generator:
            raise RuntimeError("Generator is not initialized")
        return self.generator(prompt)