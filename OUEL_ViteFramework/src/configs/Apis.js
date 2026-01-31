import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000/";

export const endpoints = {
    'check-grammar': '/gemini/writing-app/check-grammar/',
};

export default axios.create({
    baseURL: BASE_URL
});