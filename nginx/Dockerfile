FROM nginx:1.20.1
COPY --from=builder /app/build /etc/nginx/html/
CMD ["nginx", "-g", "daemon off;"]
