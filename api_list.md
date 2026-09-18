API list

1. Authentication
```
POST /auth/register
POST /auth/login
GET /auth/me
```

2. User Profile
```
GET /profile
PUT /profile
POST /profile/experience
POST /profile/training
```
3. Location
```
POST /location
GET /location
GET /location/nearby
```
4. Companies
```
GET /companies
GET /companies/{company_id}
POST /companies/scrape (if triggering scraping from backend)
```
5. Jobs
```
GET /jobs
GET /jobs/{job_id}
GET /jobs/nearby
GET /jobs/search
```
6. Skill Extraction
```
POST /skills/extract
POST /skills/extract-from-job
```
7. Skill Normalization
```
POST /skills/normalize
```
8. Skill Gap Analysis
```
POST /skill-gap/analyze
GET /skill-gap
```
9. Training Database
```
GET /trainings
GET /trainings/{training_id}
POST /trainings (government/admin)
```
10. Training Matching
```
POST /training/match
GET /training/recommended
```
11. Government Dashboard
```
GET /government/statistics
GET /government/skill-demand
GET /government/job-demand
GET /government/training-demand
```
12. Reports
```
GET /report
POST /report/generate
```