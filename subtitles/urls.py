from django.urls import path

from subtitles.view.subtitlesyncview import SubtitleSyncView

urlpatterns = [
    path("sync/", SubtitleSyncView.as_view(), name="subtitle-sync"),
]
