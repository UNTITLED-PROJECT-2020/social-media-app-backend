environments/ gives you all environments as a viewset
on environments/join you send in token in header and in data {"join":[names of env user wants to join]}
ex. you send his token and {"join":["Photo","Food","something"]} in data on environments/join
on environments/name/<name of env> you access the specific env
for example Photography whose pk is 9 can be accessed on environments/9 or on environments/name/Photo
environments/user/ gives all the connections of environments and users
like for example photo is an env with pk 1 and im a user with pk 7 and you are with pk 8 and 
there is another env with pk 2 and i have joined 1 and 2 and you have only joined 1 so environments/userenv/ will have 3 entries
you can send only the token in header with get req on environments/userenv/ and youll get all the envs that user is in