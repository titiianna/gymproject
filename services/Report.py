class ClassService:
    @staticmethod
    def _make_class_data(
        title, sport_type, coach_username,
        hall_name, day, time, capacity
    ):
        return {
            "title": title,
            "sport_type": sport_type,
            "coach_username": coach_username,
            "hall_name": hall_name,
            "day": day,
            "time": time,
            "capacity": capacity}
    @staticmethod
    def _check_class_conflict(class_data, classes_list, class_id=None):
        for current_class in classes_list :
            if current_class.class_id == class_id:
                continue
            if (current_class.day == class_data["day"]
                and current_class.time == class_data["time"]):
                if current_class.coach_username == class_data[
                    "coach_username"
                ]:
                    return False , "the instructor has another class at this time"
                if current_class.hall_name ==class_data ["hall_name"]:
                    return False , "the hall is reserved at this time"
                return True ,""
            @staticmethod
            def _check_class (class_data , users_dict , halls_dict , classes_list , 
                              class_id= None):
                title = class_data["title"]
                sport_type=class_data["sport_type"]
                coach_username= class_data["coach_username"]
                hall_name= class_data["hall_name"]
                day= class_data["day"]
                time= class_data["time"]
                capacity= class_data["capacity"]
                if not isinstance(title , str )or not title.strip():
                    return False, "The class title cannot be empty"
                valid_sports = {"fitness " , "yoga" , "boxing " , "swimming"}
                if sport_type not in valid_sports:
                    return False , "The type of sport is invalid"
                coach = users_dict.get (coach_username)
                if coach is None or coach.role != "coach":
                    return False , "No coach was found"
                if not coach.is_active :
                    return False , "The coach is not available"
                hall = halls_dict.get (hall_name)
                if hall is None :
                    return False , "The requested hall was not found"
                if not validators.day_validate (day):
                    return False , "The scheduled date is incorrect"
                if not validators.time_validate (time):
                    return False , "Incorrect scheduled time"
                if not validators.positive_int_validate (capacity):
                    return False , "The capacity must be a positive integer"
                capacity - int (capacity)
                if capacity > hall.capacity :
                    return False ,"The capacity of the classroom is greater than the capacity of the hall"
                
                

                
                

                

            

            