from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Zap, ZapRun, ZapRunOutbox

@csrf_exempt
def webhook_handler(request, user_id, zap_id):
    if request.method == "POST":
        try:
            # Parse request body
            body = json.loads(request.body)


            
            # Find the Zap instance
            zap = Zap.objects.get(id=zap_id)

            # Create a new ZapRun and ZapRunOutbox entry in a transaction
            from django.db import transaction
            with transaction.atomic():
                zap_run = ZapRun.objects.create(zap=zap, metadata=body)
                ZapRunOutbox.objects.create(zap_run=zap_run)

            return JsonResponse({"message": "Webhook received"})
        except Zap.DoesNotExist:
            return JsonResponse({"error": "Zap not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)
