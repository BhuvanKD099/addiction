const API_BASE = "http://127.0.0.1:5000";

async function apiRequest(endpoint, method = "GET", body = null, token = null){

    const headers = {
        "Content-Type":"application/json"
    };

    if(token){
        headers["Authorization"] = "Bearer " + token;
    }

    const response = await fetch(API_BASE + endpoint,{

        method:method,
        headers:headers,
        body:body ? JSON.stringify(body):null

    });

    return response.json();

}