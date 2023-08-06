# from django.contrib import admin
#
# from .models import Notification, MessageTemplate, Message
#
# # Register your models here.
#
#
# @admin.register(MessageTemplate)
# class TemplateAdmin(admin.ModelAdmin):
#     list_display = ("name", "description", "code", "title", "text", "extra")
#     list_filter = ("name", "code")
#     ordering = ("name",)
#
#
# class NotificationInline(admin.TabularInline):
#     model = Notification
#     extra = 0
#     fields = ["to", "push_state", "has_read", "is_ignored", "created_at"]
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         return qs.select_related("to")
#
#
# @admin.register(Message)
# class MessageAdmin(admin.ModelAdmin):
#     list_display = [
#         "title",
#         "msg_type",
#         "template",
#         "created_at",
#     ]
#     list_filter = ("to", "created_at")
#     search_fields = ["mark"]
#     inlines = (NotificationInline,)
#     ordering = ("-id",)
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         return qs.prefetch_related("notify")
