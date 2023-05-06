// выход, очищаются все данные о пользователе, 
// таким образом, пользователь не может получитьникакую инфомрацию
function exit(){
    sessionStorage.removeItem('clientID')
    sessionStorage.removeItem('managerID')
}