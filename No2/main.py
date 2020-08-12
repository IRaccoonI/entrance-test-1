import re
import operator

ips_count_dict = {}
number_ip_in_top = 5

with(open('./hits.txt', 'r')) as f:
    for line in f.readlines():
        match = re.match('(?P<host>.+)\t(?P<ip>.+)\t(?P<page>.+)', line)
        cur_ip = match.groupdict()['ip']

        if cur_ip not in ips_count_dict:
            ips_count_dict[cur_ip] = 1
        else:
            ips_count_dict[cur_ip] += 1

most_frequent_ip_with_count = sorted(ips_count_dict.items(), key=operator.itemgetter(1))[:-number_ip_in_top:-1]

most_frequent_ip = [i[0] for i in most_frequent_ip_with_count]
print(most_frequent_ip)