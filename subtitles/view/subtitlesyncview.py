from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json

from subtitles.services.syncer import SubtitleSyncer
from subtitles.services.cleaner import Cleaner


@method_decorator(csrf_exempt, name='dispatch')
class SubtitleSyncView(View):

    def post(self, request):
        try:

            if 'primary_subtitle' in request.FILES:
                uploaded_file = request.FILES['primary_subtitle']
                file_content = uploaded_file.read().decode('utf-8')

                try:
                    data = json.loads(file_content)
                except json.JSONDecodeError:
                    return JsonResponse({"error": "Uploaded file is not valid JSON"}, status=400)


            elif 'primary_subtitle' in request.POST:
                raw_text = request.POST.get('primary_subtitle')
                try:
                    data = json.loads(raw_text)
                except json.JSONDecodeError:
                    return JsonResponse({"error": "primary_subtitle is not valid JSON text"}, status=400)


            else:
                try:
                    body_unicode = request.body.decode('utf-8')
                    data = json.loads(body_unicode)
                except json.JSONDecodeError:
                    return JsonResponse({"error": "Request body is not valid JSON"}, status=400)

            primary_text = data.get("primary_subtitle")
            secondary_text = data.get("secondary_subtitle")  # ممکن است None باشد

            if not primary_text:
                return JsonResponse({"error": "primary_subtitle is required"}, status=400)

            cleaner = Cleaner()
            cleaned_primary = cleaner.clean(primary_text)

            if secondary_text:
                cleaned_secondary = cleaner.clean(secondary_text)
            else:
                cleaned_secondary = None

            syncer = SubtitleSyncer()
            result = syncer.sync(cleaned_primary, cleaned_secondary)

            return JsonResponse({
                "status": "success",
                "primary_caption_count": result.get("primary_caption_count", 0),
                "secondary_caption_count": result.get("secondary_caption_count", 0),
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
