def generate_prompt(past_transitions, obs, info):
    prompt = "Possible actions of the agent: {}\n".format(", ".join(info["possible_actions"]))
    prompt += "{}\n".format(info["goal"])
    for transition in past_transitions:
        prompt += "Observation: {}\n".format(', '.join(transition["obs"]))
        prompt += "Action:{}\n".format(transition["act"])

    prompt += "Observation: {}\n".format(', '.join(obs))
    prompt += "Action:"
    return prompt
def obs2text( obs):

        text = ""

        in_kitchen = obs[0]
        in_bathroom = obs[1]
        in_bedroom = obs[2]
        in_livingroom = obs[3]
        
        see_chips = obs[4]
        close_to_chips = obs[5]
        hold_chips = obs[6]
        chips_on_coffeetable = obs[7]
        
        see_milk = obs[8]
        close_to_milk = obs[9]
        hold_milk = obs[10]
        milk_on_coffeetable = obs[11]

        see_tv = obs[12]
        close_to_tv = obs[13]
        is_face_tv = obs[14]
        is_tv_on = obs[15]

        see_sofa = obs[16]
        close_to_sofa = obs[17]
        is_sit_sofa = obs[18]

        see_coffeetable = obs[19]
        close_to_coffeetable = obs[20]
        assert in_kitchen + in_bathroom + in_bedroom + in_livingroom == 1, "Only one room can be true at a time"

        # template for room
        in_room_teplate = "There are four rooms: the kitchen, bathroom, bedroom, and living room. You are in the {} "
        if in_kitchen:
            text += in_room_teplate.format("kitchen")
        elif in_bathroom:
            text += in_room_teplate.format("bathroom")
        elif in_bedroom:
            text += in_room_teplate.format("bedroom")
        elif in_livingroom:
            text += in_room_teplate.format("living room")

        ########################################template2####################################
        # template for kitchen
        object_text = ""

        action_list = []

        if in_kitchen:

            if see_chips and see_milk:
                object_text += "and notice chips and milk. "

                if hold_chips and hold_milk:
                    object_text += "Currently, you have grabbed the chips and the milk in hand. "

                    action_list = [
                        0,
                        2,
                        3,
                    ]

                elif hold_chips and not hold_milk:
                    if close_to_milk:
                        object_text += "The milk is close to you. But you have not grabbed the milk. Currently, you have grabbed the chips in hand. "

                        action_list = [
                            0,
                            2,
                            3,
                            10
                        ]
                    else:
                        object_text += "The milk is not close to you. Currently, you have grabbed the chips in hand. "

                        action_list = [
                            0,
                            2,
                            3,
                            5
                        ]
                elif not hold_chips and hold_milk:
                    if close_to_chips:
                        object_text += "The chips are close to you. But you have not grabbed the chips. Currently, you have grabbed the milk in hand. "

                        action_list = [
                            0,
                            2,
                            3,
                            9
                        ]
                    else:
                        object_text += "The chips are not close to you. Currently, you have grabbed the milk in hand. "

                        action_list = [
                            0,
                            2,
                            3,
                            4
                        ]
                else:
                    if close_to_chips and close_to_milk:
                        object_text += "They are close to you. But you have not grabbed the them. "

                        action_list = [
                            0,
                            2,
                            3,
                            9,
                            10
                        ]

                    elif close_to_chips and not close_to_milk:
                        object_text += "The chips are close to you. But you have not grabbed the chips. "

                        action_list = [
                            0,
                            2,
                            3,
                            5,
                            9,
                        ]

                    elif not close_to_chips and close_to_milk:
                        object_text += "The milk is close to you. But you have not grabbed the milk. "

                        action_list = [
                            0,
                            2,
                            3,
                            4,
                            10,
                        ]

                    else:
                        object_text += "But they are not close to you. "

                        action_list = [
                            0,
                            2,
                            3,
                            4,
                            5,
                        ]

                    object_text += "Currently, you are not grabbing anything in hand. "

            elif see_chips and not see_milk:
                object_text += "and only notice chips. "

                if hold_chips:
                    object_text += "Currently, you have grabbed the chips in hand. "

                    action_list = [
                        0,
                        2,
                        3,
                    ]

                else:
                    if close_to_chips:
                        object_text += "The chips are close to you. But you have not grabbed the chips. "

                        action_list = [
                            0,
                            2,
                            3,
                            9,
                        ]
                    else:
                        object_text += "The chips are not close to you. "

                        action_list = [
                            0,
                            2,
                            3,
                            5,
                        ]

            elif not see_chips and see_milk:
                object_text += "and notice milk. "

                if hold_milk:
                    object_text += "Currently, you have grabbed the milk in hand. "

                    action_list = [
                        0,
                        2,
                        3,
                    ]

                else:
                    if close_to_milk:
                        object_text += "The milk is close to you. But you have not grabbed the milk. "

                        action_list = [
                            0,
                            2,
                            3,
                            10,
                        ]
                    else:
                        object_text += "The milk is not close to you. "

                        action_list = [
                            0,
                            2,
                            3,
                            4,
                        ]

            else:
                object_text += "and notice nothing. "

                action_list = [
                    0,
                    2,
                    3,
                ]

        elif in_livingroom:

            object_text += "and you notice a coffee table, a TV and a sofa. "

            assert close_to_coffeetable + close_to_tv + close_to_sofa <= 1, "You are next to more than one object from coffee table, TV and sofa."
            assert see_coffeetable + see_tv + see_sofa >= 3, "You don't see coffee table, TV and sofa."

            if not close_to_coffeetable and not close_to_tv and not close_to_sofa:
                object_text += "They are not close to you. "

                if hold_chips and hold_milk:
                    object_text += "Currently, you have grabbed the chips and the milk in hand. "
                elif not hold_chips and hold_milk:
                    object_text += "Currently, you have grabbed the milk in hand. "
                elif hold_chips and not hold_milk:
                    object_text += "Currently, you have grabbed the chips in hand. "
                else:
                    object_text += "Currently, you are not grabbing anything in hand. "

                action_list = [
                    1,
                    2,
                    3,
                    6,
                    7,
                    8
                ]

            if close_to_coffeetable:

                if (chips_on_coffeetable and hold_milk) or (milk_on_coffeetable and hold_chips):
                    object_text += "The TV is not close to you. "
                else:
                    object_text += "The coffee table is close to you. "

                if hold_chips and hold_milk:
                    object_text += "Currently, you have grabbed the chips and the milk in hand. "

                    action_list = [
                        1,
                        2,
                        3,
                        7,
                        8,
                        11,
                        12
                    ]
                elif not hold_chips and hold_milk:
                    if not chips_on_coffeetable:
                        object_text += "Currently, you have grabbed the milk in hand. "

                        action_list = [
                            1,
                            2,
                            3,
                            7,
                            8,
                            12
                        ]

                    else:
                        object_text += "Currently, you have the chips on the coffee table and the milk in your hand. "

                        action_list = [
                            1,
                            2,
                            3,
                            7,
                            8,
                        ]

                elif hold_chips and not hold_milk:
                    object_text += "Currently, you have grabbed the chips in hand. "

                    if not milk_on_coffeetable:
                        object_text += "Currently, you have grabbed the chips in hand. "

                        action_list = [
                            1,
                            2,
                            3,
                            7,
                            8,
                            11
                        ]

                    else:
                        object_text += "Currently, you have the milk on the coffee table and the chips in your hand. "

                        action_list = [
                            1,
                            2,
                            3,
                            7,
                            8,
                        ]

                else:
                    object_text += "Currently, you are not grabbing anything in hand. "

                    action_list = [
                        1,
                        2,
                        3,
                    ]

            if close_to_tv:
                if is_tv_on:
                    object_text += "The sofa is not close to you. "

                    if hold_chips and hold_milk:
                        object_text += "Currently, the TV is turned on, you have grabbed the chips and the milk in hand. "

                    elif not hold_chips and hold_milk:
                        if not chips_on_coffeetable:
                            object_text += "Currently, the TV is turned on, you have grabbed the milk in hand. "
                        else:
                            object_text += "Currently, the TV is turned on, you have the chips on the coffee table and the milk in your hand. "
                    elif hold_chips and not hold_milk:
                        object_text += "Currently, the TV is turned on, you have grabbed the chips in hand. "
                        if not milk_on_coffeetable:
                            object_text += "Currently, the TV is turned on, you have grabbed the chips in hand. "
                        else:
                            object_text += "Currently, the TV is turned on, you have the milk on the coffee table and the chips in your hand. "

                    action_list = [
                        1,
                        2,
                        3,
                        6,
                        8,
                    ]

                else:
                    object_text += "The TV is close to you. "

                    if hold_chips and hold_milk:
                        object_text += "Currently, you have grabbed the chips and the milk in hand. "

                    elif not hold_chips and hold_milk:
                        if not chips_on_coffeetable:
                            object_text += "Currently, you have grabbed the milk in hand. "
                        else:
                            object_text += "Currently, you have the chips on the coffee table and the milk in your hand. "
                    elif hold_chips and not hold_milk:
                        object_text += "Currently, you have grabbed the chips in hand. "
                        if not milk_on_coffeetable:
                            object_text += "Currently, you have grabbed the chips in hand. "
                        else:
                            object_text += "Currently, you have the milk on the coffee table and the chips in your hand. "

                    action_list = [
                        1,
                        2,
                        3,
                        6,
                        8,
                        13,
                        14
                    ]

            if close_to_sofa:

                if not is_sit_sofa:
                    object_text += "The sofa is close to you. "

                    if is_tv_on:
                        if hold_chips and hold_milk:
                            object_text += "Currently, the TV is turned on, you have grabbed the chips and the milk in hand. "

                        elif not hold_chips and hold_milk:
                            if not chips_on_coffeetable:
                                object_text += "Currently, the TV is turned on, you have grabbed the milk in hand. "
                            else:
                                object_text += "Currently, the TV is turned on, you have the chips on the coffee table and the milk in your hand. "
                        elif hold_chips and not hold_milk:
                            object_text += "Currently, the TV is turned on, you have grabbed the chips in hand. "
                            if not milk_on_coffeetable:
                                object_text += "Currently, the TV is turned on, you have grabbed the chips in hand. "
                            else:
                                object_text += "Currently, the TV is turned on, you have the milk on the coffee table and the chips in your hand. "

                        action_list = [
                            1,
                            2,
                            3,
                            6,
                            7,
                            15,
                            16
                        ]
                    else:
                        if hold_chips and hold_milk:
                            object_text += "Currently, you have grabbed the chips and the milk in hand. "

                        elif not hold_chips and hold_milk:
                            if not chips_on_coffeetable:
                                object_text += "Currently, you have grabbed the milk in hand. "
                            else:
                                object_text += "Currently, you have the chips on the coffee table and the milk in your hand. "
                        elif hold_chips and not hold_milk:
                            object_text += "Currently, you have grabbed the chips in hand. "
                            if not milk_on_coffeetable:
                                object_text += "Currently, you have grabbed the chips in hand. "
                            else:
                                object_text += "Currently, you have the milk on the coffee table and the chips in your hand. "

                        action_list = [
                            1,
                            2,
                            3,
                            6,
                            7,
                        ]

                else:
                    object_text += "You are sitting on the sofa. "

                    if is_tv_on:
                        if hold_chips and hold_milk:
                            object_text += "Currently, the TV is turned on, you have grabbed the chips and the milk in hand. "

                        elif not hold_chips and hold_milk:
                            if not chips_on_coffeetable:
                                object_text += "Currently, the TV is turned on, you have grabbed the milk in hand. "
                            else:
                                object_text += "Currently, the TV is turned on, you have the chips on the coffee table and the milk in your hand. "
                        elif hold_chips and not hold_milk:
                            object_text += "Currently, the TV is turned on, you have grabbed the chips in hand. "
                            if not milk_on_coffeetable:
                                object_text += "Currently, the TV is turned on, you have grabbed the chips in hand. "
                            else:
                                object_text += "Currently, the TV is turned on, you have the milk on the coffee table and the chips in your hand. "

                        action_list = [1, 2, 3]
                    else:
                        if hold_chips and hold_milk:
                            object_text += "Currently, you have grabbed the chips and the milk in hand. "

                        elif not hold_chips and hold_milk:
                            if not chips_on_coffeetable:
                                object_text += "Currently, you have grabbed the milk in hand. "
                            else:
                                object_text += "Currently, you have the chips on the coffee table and the milk in your hand. "
                        elif hold_chips and not hold_milk:
                            object_text += "Currently, you have grabbed the chips in hand. "
                            if not milk_on_coffeetable:
                                object_text += "Currently, you have grabbed the chips in hand. "
                            else:
                                object_text += "Currently, you have the milk on the coffee table and the chips in your hand. "

                        action_list = [1, 2, 3]

        elif in_bedroom:

            if hold_chips and hold_milk:
                object_text += "and notice nothing. Currently, you have grabbed the chips and the milk in hand. "
            elif hold_chips and not hold_milk:
                object_text += "and notice nothing. Currently, you have grabbed the chips in hand. "
            elif not hold_chips and hold_milk:
                object_text += "and notice nothing. Currently, you have grabbed the milk in hand. "
            else:
                object_text += "and notice nothing. Currently, you are not grabbing anything in hand. "

            action_list = [0, 1, 2]

        elif in_bathroom:

            if hold_chips and hold_milk:
                object_text += "and notice nothing. Currently, you have grabbed the chips and the milk in hand. "
            elif hold_chips and not hold_milk:
                object_text += "and notice nothing. Currently, you have grabbed the chips in hand. "
            elif not hold_chips and hold_milk:
                object_text += "and notice nothing. Currently, you have grabbed the milk in hand. "
            else:
                object_text += "and notice nothing. Currently, you are not grabbing anything in hand. "

            action_list = [0, 1, 3]

        text += object_text

        # template for target
        target_template = "In order to enjoy the chips and the milk while watching TV, "
        text += target_template

        # template for next step
        next_step_text = "your next step is to"
        text += next_step_text

        action_template = [
            "walk to the living room", # 0
            "walk to the kitchen", # 1
            "walk to the bathroom", # 2
            "walk to the bedroom", # 3

            "walk to the chips", # 4
            "walk to the milk", # 5
            'walk to the coffee table', # 6
            'walk to the TV', # 7
            'walk to the sofa', # 8

            "grab the chips", # 9
            "grab the milk", # 10

            'put the chips on the coffee table', # 11
            'put the milk on the coffee table', # 12

            "turn on the TV", # 13
            "turn off the TV", # 14

            "sit on the sofa", # 15
            "stand up from the sofa" # 16
        ]

        template2action = {
            k:i for i,k in enumerate(action_template)
        }

        actions = [action_template[i] for i in action_list]

        return {"prompt": text, "action": actions}
def obs_to_glam_obs(obs):
        Glam_obs={"descriptions":[],'possible_actions':[],"goal":""}
        text = ""

        in_kitchen = obs[0]
        in_bathroom = obs[1]
        in_bedroom = obs[2]
        in_livingroom = obs[3]
        
        see_chips = obs[4]
        close_to_chips = obs[5]
        hold_chips = obs[6]
        chips_on_coffeetable = obs[7]
        
        see_milk = obs[8]
        close_to_milk = obs[9]
        hold_milk = obs[10]
        milk_on_coffeetable = obs[11]

        see_tv = obs[12]
        close_to_tv = obs[13]
        is_face_tv = obs[14]
        is_tv_on = obs[15]

        see_sofa = obs[16]
        close_to_sofa = obs[17]
        is_sit_sofa = obs[18]

        see_coffeetable = obs[19]
        close_to_coffeetable = obs[20]
        assert in_kitchen + in_bathroom + in_bedroom + in_livingroom == 1, "Only one room can be true at a time"

        # template for room
        in_room_teplate = "There are four rooms: the kitchen, bathroom, bedroom, and living room. You are in the {} "
        if in_kitchen:
            text += in_room_teplate.format("kitchen")
        elif in_bathroom:
            text += in_room_teplate.format("bathroom")
        elif in_bedroom:
            text += in_room_teplate.format("bedroom")
        elif in_livingroom:
            text += in_room_teplate.format("living room")

        ########################################template2####################################
        # template for kitchen
        object_text = ""

        action_list = []

        if in_kitchen:

            if see_chips and see_milk:
                object_text += "and notice chips and milk. "

                if hold_chips and hold_milk:
                    object_text += "Currently, you have grabbed the chips and the milk in hand. "

                    action_list = [
                        0,
                        2,
                        3,
                    ]

                elif hold_chips and not hold_milk:
                    if close_to_milk:
                        object_text += "The milk is close to you. But you have not grabbed the milk. Currently, you have grabbed the chips in hand. "

                        action_list = [
                            0,
                            2,
                            3,
                            10
                        ]
                    else:
                        object_text += "The milk is not close to you. Currently, you have grabbed the chips in hand. "

                        action_list = [
                            0,
                            2,
                            3,
                            5
                        ]
                elif not hold_chips and hold_milk:
                    if close_to_chips:
                        object_text += "The chips are close to you. But you have not grabbed the chips. Currently, you have grabbed the milk in hand. "

                        action_list = [
                            0,
                            2,
                            3,
                            9
                        ]
                    else:
                        object_text += "The chips are not close to you. Currently, you have grabbed the milk in hand. "

                        action_list = [
                            0,
                            2,
                            3,
                            4
                        ]
                else:
                    if close_to_chips and close_to_milk:
                        object_text += "They are close to you. But you have not grabbed the them. "

                        action_list = [
                            0,
                            2,
                            3,
                            9,
                            10
                        ]

                    elif close_to_chips and not close_to_milk:
                        object_text += "The chips are close to you. But you have not grabbed the chips. "

                        action_list = [
                            0,
                            2,
                            3,
                            5,
                            9,
                        ]

                    elif not close_to_chips and close_to_milk:
                        object_text += "The milk is close to you. But you have not grabbed the milk. "

                        action_list = [
                            0,
                            2,
                            3,
                            4,
                            10,
                        ]

                    else:
                        object_text += "But they are not close to you. "

                        action_list = [
                            0,
                            2,
                            3,
                            4,
                            5,
                        ]

                    object_text += "Currently, you are not grabbing anything in hand. "

            elif see_chips and not see_milk:
                object_text += "and only notice chips. "

                if hold_chips:
                    object_text += "Currently, you have grabbed the chips in hand. "

                    action_list = [
                        0,
                        2,
                        3,
                    ]

                else:
                    if close_to_chips:
                        object_text += "The chips are close to you. But you have not grabbed the chips. "

                        action_list = [
                            0,
                            2,
                            3,
                            9,
                        ]
                    else:
                        object_text += "The chips are not close to you. "

                        action_list = [
                            0,
                            2,
                            3,
                            5,
                        ]

            elif not see_chips and see_milk:
                object_text += "and notice milk. "

                if hold_milk:
                    object_text += "Currently, you have grabbed the milk in hand. "

                    action_list = [
                        0,
                        2,
                        3,
                    ]

                else:
                    if close_to_milk:
                        object_text += "The milk is close to you. But you have not grabbed the milk. "

                        action_list = [
                            0,
                            2,
                            3,
                            10,
                        ]
                    else:
                        object_text += "The milk is not close to you. "

                        action_list = [
                            0,
                            2,
                            3,
                            4,
                        ]

            else:
                object_text += "and notice nothing. "

                action_list = [
                    0,
                    2,
                    3,
                ]

        elif in_livingroom:

            object_text += "and you notice a coffee table, a TV and a sofa. "

            assert close_to_coffeetable + close_to_tv + close_to_sofa <= 1, "You are next to more than one object from coffee table, TV and sofa."
            assert see_coffeetable + see_tv + see_sofa >= 3, "You don't see coffee table, TV and sofa."

            if not close_to_coffeetable and not close_to_tv and not close_to_sofa:
                object_text += "They are not close to you. "

                if hold_chips and hold_milk:
                    object_text += "Currently, you have grabbed the chips and the milk in hand. "
                elif not hold_chips and hold_milk:
                    object_text += "Currently, you have grabbed the milk in hand. "
                elif hold_chips and not hold_milk:
                    object_text += "Currently, you have grabbed the chips in hand. "
                else:
                    object_text += "Currently, you are not grabbing anything in hand. "

                action_list = [
                    1,
                    2,
                    3,
                    6,
                    7,
                    8
                ]

            if close_to_coffeetable:

                if (chips_on_coffeetable and hold_milk) or (milk_on_coffeetable and hold_chips):
                    object_text += "The TV is not close to you. "
                else:
                    object_text += "The coffee table is close to you. "

                if hold_chips and hold_milk:
                    object_text += "Currently, you have grabbed the chips and the milk in hand. "

                    action_list = [
                        1,
                        2,
                        3,
                        7,
                        8,
                        11,
                        12
                    ]
                elif not hold_chips and hold_milk:
                    if not chips_on_coffeetable:
                        object_text += "Currently, you have grabbed the milk in hand. "

                        action_list = [
                            1,
                            2,
                            3,
                            7,
                            8,
                            12
                        ]

                    else:
                        object_text += "Currently, you have the chips on the coffee table and the milk in your hand. "

                        action_list = [
                            1,
                            2,
                            3,
                            7,
                            8,
                        ]

                elif hold_chips and not hold_milk:
                    object_text += "Currently, you have grabbed the chips in hand. "

                    if not milk_on_coffeetable:
                        object_text += "Currently, you have grabbed the chips in hand. "

                        action_list = [
                            1,
                            2,
                            3,
                            7,
                            8,
                            11
                        ]

                    else:
                        object_text += "Currently, you have the milk on the coffee table and the chips in your hand. "

                        action_list = [
                            1,
                            2,
                            3,
                            7,
                            8,
                        ]

                else:
                    object_text += "Currently, you are not grabbing anything in hand. "

                    action_list = [
                        1,
                        2,
                        3,
                    ]

            if close_to_tv:
                if is_tv_on:
                    object_text += "The sofa is not close to you. "

                    if hold_chips and hold_milk:
                        object_text += "Currently, the TV is turned on, you have grabbed the chips and the milk in hand. "

                    elif not hold_chips and hold_milk:
                        if not chips_on_coffeetable:
                            object_text += "Currently, the TV is turned on, you have grabbed the milk in hand. "
                        else:
                            object_text += "Currently, the TV is turned on, you have the chips on the coffee table and the milk in your hand. "
                    elif hold_chips and not hold_milk:
                        object_text += "Currently, the TV is turned on, you have grabbed the chips in hand. "
                        if not milk_on_coffeetable:
                            object_text += "Currently, the TV is turned on, you have grabbed the chips in hand. "
                        else:
                            object_text += "Currently, the TV is turned on, you have the milk on the coffee table and the chips in your hand. "

                    action_list = [
                        1,
                        2,
                        3,
                        6,
                        8,
                    ]

                else:
                    object_text += "The TV is close to you. "

                    if hold_chips and hold_milk:
                        object_text += "Currently, you have grabbed the chips and the milk in hand. "

                    elif not hold_chips and hold_milk:
                        if not chips_on_coffeetable:
                            object_text += "Currently, you have grabbed the milk in hand. "
                        else:
                            object_text += "Currently, you have the chips on the coffee table and the milk in your hand. "
                    elif hold_chips and not hold_milk:
                        object_text += "Currently, you have grabbed the chips in hand. "
                        if not milk_on_coffeetable:
                            object_text += "Currently, you have grabbed the chips in hand. "
                        else:
                            object_text += "Currently, you have the milk on the coffee table and the chips in your hand. "

                    action_list = [
                        1,
                        2,
                        3,
                        6,
                        8,
                        13,
                        14
                    ]

            if close_to_sofa:

                if not is_sit_sofa:
                    object_text += "The sofa is close to you. "

                    if is_tv_on:
                        if hold_chips and hold_milk:
                            object_text += "Currently, the TV is turned on, you have grabbed the chips and the milk in hand. "

                        elif not hold_chips and hold_milk:
                            if not chips_on_coffeetable:
                                object_text += "Currently, the TV is turned on, you have grabbed the milk in hand. "
                            else:
                                object_text += "Currently, the TV is turned on, you have the chips on the coffee table and the milk in your hand. "
                        elif hold_chips and not hold_milk:
                            object_text += "Currently, the TV is turned on, you have grabbed the chips in hand. "
                            if not milk_on_coffeetable:
                                object_text += "Currently, the TV is turned on, you have grabbed the chips in hand. "
                            else:
                                object_text += "Currently, the TV is turned on, you have the milk on the coffee table and the chips in your hand. "

                        action_list = [
                            1,
                            2,
                            3,
                            6,
                            7,
                            15,
                            16
                        ]
                    else:
                        if hold_chips and hold_milk:
                            object_text += "Currently, you have grabbed the chips and the milk in hand. "

                        elif not hold_chips and hold_milk:
                            if not chips_on_coffeetable:
                                object_text += "Currently, you have grabbed the milk in hand. "
                            else:
                                object_text += "Currently, you have the chips on the coffee table and the milk in your hand. "
                        elif hold_chips and not hold_milk:
                            object_text += "Currently, you have grabbed the chips in hand. "
                            if not milk_on_coffeetable:
                                object_text += "Currently, you have grabbed the chips in hand. "
                            else:
                                object_text += "Currently, you have the milk on the coffee table and the chips in your hand. "

                        action_list = [
                            1,
                            2,
                            3,
                            6,
                            7,
                        ]

                else:
                    object_text += "You are sitting on the sofa. "

                    if is_tv_on:
                        if hold_chips and hold_milk:
                            object_text += "Currently, the TV is turned on, you have grabbed the chips and the milk in hand. "

                        elif not hold_chips and hold_milk:
                            if not chips_on_coffeetable:
                                object_text += "Currently, the TV is turned on, you have grabbed the milk in hand. "
                            else:
                                object_text += "Currently, the TV is turned on, you have the chips on the coffee table and the milk in your hand. "
                        elif hold_chips and not hold_milk:
                            object_text += "Currently, the TV is turned on, you have grabbed the chips in hand. "
                            if not milk_on_coffeetable:
                                object_text += "Currently, the TV is turned on, you have grabbed the chips in hand. "
                            else:
                                object_text += "Currently, the TV is turned on, you have the milk on the coffee table and the chips in your hand. "

                        action_list = [1, 2, 3]
                    else:
                        if hold_chips and hold_milk:
                            object_text += "Currently, you have grabbed the chips and the milk in hand. "

                        elif not hold_chips and hold_milk:
                            if not chips_on_coffeetable:
                                object_text += "Currently, you have grabbed the milk in hand. "
                            else:
                                object_text += "Currently, you have the chips on the coffee table and the milk in your hand. "
                        elif hold_chips and not hold_milk:
                            object_text += "Currently, you have grabbed the chips in hand. "
                            if not milk_on_coffeetable:
                                object_text += "Currently, you have grabbed the chips in hand. "
                            else:
                                object_text += "Currently, you have the milk on the coffee table and the chips in your hand. "

                        action_list = [1, 2, 3]

        elif in_bedroom:

            if hold_chips and hold_milk:
                object_text += "and notice nothing. Currently, you have grabbed the chips and the milk in hand. "
            elif hold_chips and not hold_milk:
                object_text += "and notice nothing. Currently, you have grabbed the chips in hand. "
            elif not hold_chips and hold_milk:
                object_text += "and notice nothing. Currently, you have grabbed the milk in hand. "
            else:
                object_text += "and notice nothing. Currently, you are not grabbing anything in hand. "

            action_list = [0, 1, 2]

        elif in_bathroom:

            if hold_chips and hold_milk:
                object_text += "and notice nothing. Currently, you have grabbed the chips and the milk in hand. "
            elif hold_chips and not hold_milk:
                object_text += "and notice nothing. Currently, you have grabbed the chips in hand. "
            elif not hold_chips and hold_milk:
                object_text += "and notice nothing. Currently, you have grabbed the milk in hand. "
            else:
                object_text += "and notice nothing. Currently, you are not grabbing anything in hand. "

            action_list = [0, 1, 3]

        text += object_text
        Glam_obs["descriptions"].append(text)
        target_template = "In order to enjoy the chips and the milk while watching TV, "
        Glam_obs["goal"] = target_template

        # template for next step
        next_step_text = "your next step is to"
        text += next_step_text

        action_template = [
            "walk to the living room", # 0
            "walk to the kitchen", # 1
            "walk to the bathroom", # 2
            "walk to the bedroom", # 3

            "walk to the chips", # 4
            "walk to the milk", # 5
            'walk to the coffee table', # 6
            'walk to the TV', # 7
            'walk to the sofa', # 8

            "grab the chips", # 9
            "grab the milk", # 10

            'put the chips on the coffee table', # 11
            'put the milk on the coffee table', # 12

            "turn on the TV", # 13
            "turn off the TV", # 14

            "sit on the sofa", # 15
            "stand up from the sofa" # 16
        ]

        template2action = {
            k:i for i,k in enumerate(action_template)
        }

        actions = [action_template[i] for i in action_list]

        Glam_obs["possible_actions"]=actions

        return Glam_obs