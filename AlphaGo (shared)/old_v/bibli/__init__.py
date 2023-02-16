import jsonpickle as jp

def obj_print(obj, context = ''):
    attrs = vars(obj)
    context = f'\n[{context}]========================'
    # print(context+',\n------->'.join("%s: %s" %
    #         item for item in attrs.items()))
    print(context)
    # json_str = f'player {obj.player}'
    json_str = jp.encode(obj, max_depth=3)
    print(json_str)
    print('========================================\n\n')