from django.core.paginator import Paginator
class Key:

    @classmethod
    def check_required_keys(cls, givin_keys, goal_keys):
        missed_keys = goal_keys.copy()
        for key in givin_keys.keys():
            if key in goal_keys:
                missed_keys.remove(key)
        return missed_keys

    @classmethod
    def add_key_to_list(cls, context, key, val):
        # new_dict = dict()
        # new_dict[key] = val
        for i in range(0, len(context)):
            context[i][key] = val
            # context[i].append

        # for item in context:
        #     item.append(new_dict)
        return context
    
    @classmethod
    def merge_dicts(cls, d1, d2):
        for item in d2:
            d1.append(item)
        return d1


class QueryString:

    @classmethod
    def create_query_string(cls, expected_keys, query_dict):
        query_string = []
        for key in query_dict:
            if key in expected_keys:
                value = query_dict[key]
                query_string.extend('%s="%s"' % (key, value))
        return query_string

    @classmethod
    def remove_keys(cls, allowed, to_remove, query_dict):
        keys = query_dict.copy().keys()
        for key in keys:
            if key not in allowed or key in to_remove:
                del query_dict[key]

    @classmethod
    def replace_min_max_with_lte_gte(cls, query_dict):
        qd = query_dict.copy()
        for key in query_dict.keys():
            if key.endswith('__min'):
                new_key = key.replace('__min', '__gte')
                value = qd[key]
                del qd[key]
                qd[new_key] = value
            elif key.endswith('__max'):
                new_key = key.replace('__max', '__lte')
                value = qd[key]
                del qd[key]
                qd[new_key] = value
        return qd
    
    @staticmethod
    def handle_ordering_keys_acc_decc_dicts(query_dict):
        qd = query_dict.copy()
        for key in query_dict.keys():
            if key.startswith('acc__'):
                new_key = key.replace('acc__', '')
                value = qd[key]
                del qd[key]
                qd[new_key] = value
            elif key.startswith('decc__'):
                new_key = key.replace('decc__', '-')
                value = qd[key]
                del qd[key]
                qd[new_key] = value
        return qd

    @staticmethod
    def handle_ordering_keys_acc_decc_string(givin_value):
        if givin_value.startswith('acc__'):
            givin_value = givin_value.replace('acc__', '')
        elif givin_value.startswith('decc__'):
            givin_value = givin_value.replace('decc__', '-')
        return givin_value


class PaginatorView:
    @classmethod
    def serializer_paginator(cls, serializer_data, page, num=10):
        paginator = Paginator(serializer_data, num)
        number = int(paginator.num_pages) 
        cur_page = int(page) if int(page) <= number else number
        data = paginator.page(cur_page)
        serializer_page_data = []
        for obj in data.object_list:
            serializer_page_data.append(dict(obj))
        
        return serializer_page_data, cur_page, number

    @classmethod
    def queryset_paginator(cls, queryset, page, num=10, return_last=True):
        paginator = Paginator(queryset, num)
        number = int(paginator.num_pages)
        if return_last:
            cur_page = int(page) if int(page) <= number else number
        else:
            cur_page = page
        try:
            queryset = paginator.page(cur_page)
        except Exception as e:
            print(e)
            return None, cur_page, number
        return queryset, cur_page, number