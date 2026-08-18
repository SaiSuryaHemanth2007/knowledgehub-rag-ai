import axios from "axios";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

api.interceptors.request.use(
  (config) => {
    if (
      config.data instanceof FormData
    ) {
      config.headers.delete?.(
        "Content-Type"
      );
    } else {
      config.headers.set?.(
        "Content-Type",
        "application/json"
      );
    }

    return config;
  }
);

export default api;