@staticmethod
def generate_reports(user_dict , classes_list , payments_list):
       active_members = sum(
        user.role == ROLE_MEMBER and user.is_active
        for user in users_dict.values())
       active_coaches=sum (user.role == ROLE_COACH and user.is_active 
                           for user in user_dict.values())
       active_classes = sum (class_session.is_active 
                             for class_session in classes_list)
       total_income = sum(payment.amount for payment in payments_list)
       return{"active_members ":active_members ,
              "active_coaches":active_coaches ,
              "active_classes":active_classes, 
              "total_income ":total_income , }
@staticmethod
def advanced_reports(classes_list , payments_list ):
       enrollments_per_class={}
       for class_session in classes_list:
              title=class_session.title 
              active_count= len(class_session.active_member_username())
              enrollments_per_class[title]=(
                     enrollments_per_class.get(title , 0 )+active_count )
              
              income_by_plan={}
              for payment in payments_list:
                     plan_title= payment.plan_title 
                     income_by_plan[plan_title]= (
                            income_by_plan.get (plan_title , 0 )+
                            payment.amount 
                     )
              top_class = None
              for title , count in enrollments_per_class.items():
                     if count >0 and (top_class is None or count>
                                      enrollments_per_class[top_class]):
                            top_class= title
                            return {
        "enrollments_per_class": enrollments_per_class,
        "income_by_plan": income_by_plan,
        "top_class": top_class,}



       
       
       