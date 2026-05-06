# Polaris' Portfolio Website

A modern full-stack portfolio website built with Django, Docker, and Caddy.

This repository contains the source code for my personal portfolio website, used to showcase projects, technical experiments, and full-stack development work.

---

## Live Site

[Polaris' Portfolio](https://polarispall.com)

---

## Modularity

The website is designed around a modular Django architecture where content, projects, and site sections are driven through Django models and managed entirely through the Django admin interface.

This structure allows the portfolio to be updated, expanded, and reorganized without directly modifying frontend templates or application logic, making the site easier to maintain and scale over time.

---

## Tech Stack

### Backend & Databases

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)

---

### Frontend

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

---

### Infrastructure & Deployment

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Caddy](https://img.shields.io/badge/Caddy-1F88C0?style=for-the-badge&logo=caddy&logoColor=white)

---

## Currently Hosted

The portfolio is currently hosted on an AWS EC2 instance running Debian Linux.

The production stack uses Docker and Docker Compose for container orchestration, with Caddy acting as the reverse proxy and automatic HTTPS provider through Let's Encrypt.

Cloudflare DNS and Cloudflared are used for domain routing and DNS management.

### Hosting Stack

![AWS](https://img.shields.io/badge/AWS_EC2-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)
![Debian](https://img.shields.io/badge/Debian-A81D33?style=for-the-badge&logo=debian&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Caddy](https://img.shields.io/badge/Caddy-1F88C0?style=for-the-badge&logo=caddy&logoColor=white)
![Cloudflare](https://img.shields.io/badge/Cloudflare-F38020?style=for-the-badge&logo=cloudflare&logoColor=white)

---

## License

This project is licensed under the MIT License.
