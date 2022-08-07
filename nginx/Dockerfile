FROM nginx:1.20.1
COPY --from=builder /app/build /etc/nginx/html/
CMD ["sudo", "nginx", "-g", "daemon off;"]
