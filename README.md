# Django AI Powered Recruitment Platform

![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

## Overview

A modern recruitment platform built in **vanilla Django**. It includes **AI-powered features**, such as CV parsing, job matching, and chat-based career advice, while keeping the current Django structure. This document provides enough detail for another developer to reproduce the system.

---

## 🚀 Features

### Candidates

* Register / Login / Logout
* Create & update profile
* Upload CV / resume (stored in S3 / local storage)
* Browse jobs and save favorites
* Apply directly from dashboard
* View AI-generated job recommendations

### Employers / Recruiters

* Register / Login / Logout
* Create / manage company profile
* Post jobs
* View applicants
* Shortlist candidates
* Recruiter dashboard with analytics
* Option to enable AI-assisted candidate suggestions

### AI & Advanced Features

* CV / resume parsing (extract skills, experience, education)
* AI job matching engine
* AI chat interface for career advice
* Vector search for semantic job matching
* Notifications (email / in-app) for application updates
* Job scraping from external portals (optional)

---

## 📦 Project Structure

```
project/
├── accounts/           # User auth, profiles, roles
├── applications/       # Job applications & AI matching
│   ├── services/       # AI matching, embeddings, CV parser
├── chat/               # AI chat endpoints
│   ├── services/       # Chat handler, message processing
├── jobs/               # Job listings, posting, search
│   ├── services/       # Job scraping, AI job parser
├── companies/          # Company management
├── notifications/      # Email & in-app notifications
├── search/             # Vector-based search & semantic job search
├── shortlisting/       # Candidate shortlist management
├── payments/           # Subscription & payment handling (optional)
├── integrations/       # Third-party integrations (Google, job boards)
├── config/             # Django settings, URL routing, storage backends
├── templates/          # UI templates
├── static/             # CSS, JS, icons, images
└── manage.py
```

---

## 🔗 API / Endpoint Blueprint

**Candidate Endpoints:**

| Method | URL                          | Description              |
| ------ | ---------------------------- | ------------------------ |
| GET    | `/api/candidate/profile/`    | Get candidate profile    |
| POST   | `/api/candidate/profile/`    | Update profile           |
| POST   | `/api/candidate/resume/`     | Upload CV / resume       |
| GET    | `/api/jobs/recommendations/` | AI-generated job matches |
| POST   | `/api/applications/apply/`   | Apply for a job          |
| GET    | `/api/applications/`         | List my applications     |

**Employer Endpoints:**

| Method | URL                                  | Description          |
| ------ | ------------------------------------ | -------------------- |
| GET    | `/api/employer/jobs/`                | List posted jobs     |
| POST   | `/api/employer/jobs/`                | Post a new job       |
| GET    | `/api/employer/job/<id>/applicants/` | List applicants      |
| POST   | `/api/employer/job/<id>/shortlist/`  | Shortlist candidates |

**AI / Chat Endpoints:**

| Method | URL                          | Description                  |
| ------ | ---------------------------- | ---------------------------- |
| POST   | `/api/chat/send/`            | Send message to AI chatbot   |
| POST   | `/api/chat/recommend/`       | AI-based job / career advice |
| POST   | `/api/match/cv/`             | Submit CV for AI matching    |
| GET    | `/api/match/<user_id>/jobs/` | Get AI job recommendations   |

**Search / Vector Search Endpoints:**

| Method | URL                       | Description                              |
| ------ | ------------------------- | ---------------------------------------- |
| GET    | `/api/search/jobs/`       | Keyword / semantic search for jobs       |
| GET    | `/api/search/candidates/` | Keyword / semantic search for candidates |

---

## 🔧 Services & AI Modules

**applications/services/**

* `ai_match.py` – Match candidates to jobs using embeddings
* `embeddings.py` – Generate vector embeddings for resumes and job descriptions
* `parser.py` – Extract structured data from resumes
* `s3_helpers.py` – Upload / retrieve resumes from storage

**chat/services/**

* `ai_chat_handler.py` – Process AI chat messages
* Handles conversation context per user

**jobs/services/**

* `ai_job_parser.py` – Extract job details from postings
* `recruiter_api.py` – Interact with external job board APIs

**search/services/**

* `vector_search.py` – Semantic search using embeddings

---

## 🔐 Roles

**Candidate**

* Profile creation & management
* Job search & AI recommendations
* Application tracking

**Employer**

* Company profile
* Job posting
* Applicant management
* Shortlisting & analytics

---

## 📊 Roadmap

* [ ] AI CV parsing and matching
* [ ] AI chat for career guidance
* [ ] Job scraping from external boards
* [ ] Email / in-app notifications
* [ ] Application status tracking
* [ ] Recruiter analytics dashboard
* [ ] API for mobile / React frontend

---

## ⚙️ Deployment

* PostgreSQL (production) / SQLite (development)
* Gunicorn + Nginx
* Dockerized for easy deployment
* AWS S3 or equivalent for resume storage

---
