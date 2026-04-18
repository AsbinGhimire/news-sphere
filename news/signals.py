from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Article
from .utils import AIService

@receiver(pre_save, sender=Article)
def automate_ai_fields(sender, instance, **kwargs):
    # Only run if content is present and AI fields are empty
    if instance.content:
        # Generate summary if empty
        if not instance.ai_summary:
            instance.ai_summary = AIService.generate_summary(instance.content)
            
        # Generate paraphrase if empty
        if not instance.paraphrased_content:
            instance.paraphrased_content = AIService.generate_paraphrase(instance.content)
