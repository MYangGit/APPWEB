import axios from 'axios';
import Cookies from 'js-cookie';

axios.defaults.timeout = 900000;

axios.interceptors.request.use(
    (config) => {
        const token = Cookies.get('token_mohub').replaceAll('%22', '');
        if (token) {
            config.headers.token = token;
        }
        return config;
    },
    (error) => Promise.reject(error),
);

export default axios;
