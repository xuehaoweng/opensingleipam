from rest_framework import serializers

from users.models import OpLogs


class OpLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpLogs
        fields = ('re_url', 're_ip', 're_method', 'rp_code', 're_content','access_time','id')
        # fields = '__all__'
        # read_only_fields = ('created', 'modified')
