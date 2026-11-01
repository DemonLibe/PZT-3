import re,sys
def key(code):
    return ('Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,'
            '"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,'
            f'"keycode":0,"physical_keycode":{code},"key_label":0,"unicode":0,"location":0,"echo":false,"script":null)')
actions=[("move_forward",87),("move_back",83),("move_left",65),("move_right",68),
         ("sprint",4194325),("crouch",4194326),("interact",69),("flashlight",70),
         ("rest",90),("radio_reply",82),("squad_follow",49),("squad_hold",50),("debug_hud",4194334),("debug_skip_hour",4194339)]
import os; p=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'project.godot'); s=open(p).read()
block='[input]\n\n'+''.join(f'{n}={{\n"deadzone": 0.2,\n"events": [{key(c)}\n]\n}}\n' for n,c in actions)
s=re.sub(r'\[input\]\n.*?(?=\n\[|\Z)', block.rstrip('\n'), s, flags=re.S)
open(p,'w').write(s.rstrip('\n')+'\n')
