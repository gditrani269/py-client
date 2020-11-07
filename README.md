llamada a la api de OS:
formato general:

curl -k -H "Authorization: Bearer Peqgar_aqui_el_token" -H 'Accept: application/json' "dominio_de_OS/apis/user.openshift.io/v1/users/~"

por ej:
curl -k \
-H "Authorization: Bearer aauvzkixX4tXpO0ZvnvvKKonyBA5yBeRN7NVe2sdw_0" \
-H 'Accept: application/json' \
"https://2886795266-8443-frugo02.environments.katacoda.com/apis/user.openshift.io/v1/users/~"

para obtener el log de un POD la estructura de la API es:
api/v1/namespaces/{namespace}/pods/{name}/log  completar nombre del proyecto en {namespace} y nombre completo del pod en {name}

curl -k \
-H "Authorization: Bearer aauvzkixX4tXpO0ZvnvvKKonyBA5yBeRN7NVe2sdw_0" \
-H 'Accept: application/json' \
"https://2886795266-8443-frugo02.environments.katacoda.com/api/v1/namespaces/ser/pods/mi-1-6mn4b/log
