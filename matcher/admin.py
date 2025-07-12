# matcher/admin.py

from django.contrib import admin
from .models import Resume, ResumeMatch

# Inline: Show matches under Resume
class ResumeMatchInline(admin.TabularInline):
    model = ResumeMatch
    extra = 0
    can_delete = False
    readonly_fields = ('role', 'score', 'category')
    show_change_link = False  # optional: no link to detail view

# Main Resume Admin View
@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploaded_at')  # shown in list view
    readonly_fields = ('uploaded_at',)
    inlines = [ResumeMatchInline]

# ResumeMatch Admin (read-only)
@admin.register(ResumeMatch)
class ResumeMatchAdmin(admin.ModelAdmin):
    list_display = ('resume', 'role', 'score', 'category')
    readonly_fields = ('resume', 'role', 'score', 'category')

    # Disable adding new ResumeMatch manually
    def has_add_permission(self, request):
        return False

    # Optional: disable editing as well
    def has_change_permission(self, request, obj=None):
        return False

from django.contrib import admin

# ✅ Custom admin panel titles
admin.site.site_header = "Resume Matcher Admin"
admin.site.site_title = "Resume Matcher Portal"
admin.site.index_title = "Welcome to Resume Scoring Admin"
