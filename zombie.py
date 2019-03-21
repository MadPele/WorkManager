# <body background="{% static 'back1.jpg' %}" style='background-repeat: no-repeat; background-size: cover; font-size: 20px'>
#
#     <div class="container">
#         <div class="row">
#             <div class="col-6"></div>
#                 <div class="cont"><p class='left'>Loged as {{ logged }}</p> <p class="right"><a href="{% url 'logout' %}">Logout</a> </p>
#                 </div>
#                 {% block menu %}
#                     <a href="{% url 'home' %}">Home</a>&emsp;<a href="{% url 'project-site' %}">Projects</a>&emsp;
#                     <a href="{% url 'employee-site' %}">Employees</a>&emsp;<a href="{% url 'productionline-site' %}">Production lines</a>
#                     &emsp;<a href="{% url 'raport-site' %}">Raports</a>
#                 {% endblock %}<br><br><br><br>
#                 <h2><center>{% block title %} Title {% endblock %}</center></h2><br><br>
#                 {% block content %} Pla {% endblock %}<br><br><br><br>
#                 {% block footer %}<div class="cont"><p class="left">Created by Andrzej Derela</p><p class="right">Today is: {{ date }}</p></div>{% endblock %}
#         </div>
#     </div>


# < !-- < style > -->
# < !--.left
# {-->
# < !--float: left;
# -->
# < !--width: 50 %;
# -->
# < !--}-->
# < !--.right
# {-->
# < !--float: left;
# -->
# < !--width: 50 %;
# -->
# < !--text - align: right;
# -->
# < !--}-->
# < !--.cont::after
# {-->
# < !--content: '';
# -->
# < !--display: block;
# -->
# < !--clear: both;
# -->
# < !--}-->
# < !--.cont
# {-->
# < !--font - size: 15
# px;
# -->
# < !--}-->
# < !-- < / style > -->