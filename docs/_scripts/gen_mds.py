__author__ = "Sander Schulhoff"
__email__ = "sanderschulhoff@gmail.com"

from pydoc import doc
import gym
import os
from os import mkdir, path

import re
import numpy as np
from utils import trim
LAYOUT = "env"

pattern = re.compile(r'(?<!^)(?=[A-Z])')

for env_spec in gym.envs.registry.all():

    try:
        # if "ALE" in str(env_spec) or "deterministic" in str(env_spec) or "frameskip" in str(env_spec):
        #     continue
        # if env_spec.id != "LunarLanderContinuous-v2":
        #     continue

        env = gym.make(env_spec.id)

        # varients dont get their own pages
        e_n = str(env_spec).lower()
        if "continuous" in e_n or "hardcore" in e_n:
            continue
        
        # print(type(en))
        docstring = trim(env.unwrapped.__doc__)
        
        split = str(type(env.unwrapped)).split(".")
        # pascal case
        pascal_env_name = env_spec.id.split("-")[0]
        snake_env_name = pattern.sub('_', pascal_env_name).lower()
        title_env_name = snake_env_name.replace("_", " ").title()
        # env_name = env.unwrapped.__class__.__name__
        env_type = split[2]
        print(env_type)
        if env_type == "atari" or env_type == "mujoo":
            continue
        # print(title_env_name)

        # exit()
        # if env_name == "environment":
        #     env_name = env_spec.id.split("-")[0]
        #     camel_env_name = env_name
        #     env_name = pattern.sub('_', env_name).lower().replace("a_l_e/_", "")
        # else:
        #     camel_env_name = env_spec.id.split("-")[0]
        
        
        # path for saving video
        v_path = os.path.join("..", "pages", "environments", env_type, snake_env_name + ".md")
        
        if os.path.exists(v_path):
            continue
    
        front_matter = "---\n"

        front_matter+= "AUTOGENERATED: DO NOT EDIT FILE DIRECTLY\n"

        front_matter+= f"layout: {LAYOUT}\n"

        front_matter+= f"title: {title_env_name}\n"
        
        front_matter+= "grid:\n"
        
        front_matter+= f"   - Action Space: {env.action_space}\n"
        
        if env.observation_space.shape:
            front_matter+= f"   - Observation Shape: {env.observation_space.shape}\n"

            if hasattr(env.observation_space, "high"):
                high = env.observation_space.high
                
                if hasattr(high, "shape"):
                    if len(high.shape) == 3:
                        high = high[0][0][0]
                high = np.round(high, 2)
                front_matter+= f"   - Observation High: {high}\n"
            
            if hasattr(env.observation_space, "low"):
                low = env.observation_space.low
                if hasattr(low, "shape"):
                    if len(low.shape) == 3:
                        low = low[0][0][0]
                low = np.round(low, 2)
                front_matter+= f"   - Observation Low: {low}\n"
        else:
            front_matter+= f"   - Observation Space: {env.observation_space}\n"

        front_matter+= f"   - Import: <code>gym.make(\"{env_spec.id}\")</code>\n"

        front_matter += "---\n"
        if docstring == None:
            docstring = "No information provided"
        all_text = front_matter + docstring

        file = open(v_path, "w")
        file.write(all_text)
        file.close()
    except Exception as e:
        print(e)
                

            
