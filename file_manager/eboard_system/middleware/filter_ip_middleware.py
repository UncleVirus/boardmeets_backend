from django.core.exceptions import PermissionDenied
from django.utils.deprecation import MiddlewareMixin
from accounts.models import IpAddress,OrganizationSetting

class FilterIPMiddleware(MiddlewareMixin):
    # Check if client IP address is allowed
    def process_request(self, request):
        orgsettings = OrganizationSetting.objects.all()
        if orgsettings:
            for i in orgsettings:
                if i.ip_filtering == True:
                    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                    if x_forwarded_for:
                        ip = x_forwarded_for.split(',')[0]
                    else:
                        ip = request.META.get('REMOTE_ADDR')
                    
                    allowed_ip_range = IpAddress.objects.all()
                    
                    print(ip)
                    def ip_to_int(ip):
                        val = 0
                        for i, s in enumerate(ip.split('.')):
                            val += int(s) * 256 ** (3 - i)
                        return val

                    def int_to_ip(val):
                        octets = []
                        for i in range(4):
                            octets.append(str(val % 256))
                            val = val >> 8
                        return '.'.join(reversed(octets))

                    def findIPs(start, end):
                        for i in range(ip_to_int(start), ip_to_int(end) + 1):
                            yield int_to_ip(i)
                    for r in allowed_ip_range:
                        print(list(findIPs(r.ip_start,r.ip_end)))
                        all_allowed_ips = list(findIPs(r.ip_start,r.ip_end))
                        if ip not in all_allowed_ips:
                            print(">>>>>NOT ALLOWED>>>>>>>>.")
                            raise PermissionDenied # If user is not allowed raise Error
                        else:
                            return None
                else:
                    return None
        else:
            return None