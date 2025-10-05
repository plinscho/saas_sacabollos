# Objetivo MVP

- Permitir que chapistas autónomos creen perfil y portafolio.
- Permitir que empresas creen ofertas de trabajo (localización, tiempo estimado, presupuesto).
- Permitir que chapistas presenten propuestas (presupuesto / plazo) a ofertas.

---

## Flujo Básico

1. Empresa publica oferta
2. Chapistas postulan
3. Empresa acepta propuesta
4. Marcar trabajo como completado
5. Dejar reseña

> Búsqueda básica de chapistas/ofertas por localización y filtros.

---

## Apps Backend Recomendadas

- **users**: autenticación, roles, datos básicos de usuario (ya presente)
- **profiles**: perfiles extendidos para chapistas y empresas
- **companies**: datos de empresas
- **jobs (offers)**: ofertas de trabajo
- **proposals (bids)**: propuestas de chapistas
- **portfolios**: trabajos y fotos subidas por chapistas
- **reviews**: valoraciones y comentarios
- **locations**: ciudades/zonas, o geo-coords (ya presente)
- **notifications**: notificaciones internas
- **payments**: manejo de pagos/impago/garantías (opcional en MVP)

---

## Modelos Recomendados (MVP mínimo)

### User (extiende AbstractUser)
- `id`, `email`, `username`, `password`, `role` {chapista, company, admin}
- Campos básicos y flags

### ChapistaProfile
- `user` (FK → User, unique)
- `display_name`, `phone`, `bio`, `servicios_ofrecidos` (tags), `precio_hora_estimado`, `rating_promedio`
- `is_verified` (documentación)
- `location` (FK → Location o lat/lng)
- `disponibilidad` (boolean / horario)

### CompanyProfile
- `user` (FK → User)
- `company_name`, `contact_person`, `phone`, `address`, `verified`

### Location
- `city`, `province`, `country`, `lat`, `lng`, `postal_code`

### JobOffer
- `id`, `company` (FK → CompanyProfile), `title`, `description`, `location` (FK → Location o text)
- `budget_min`, `budget_max`, `estimated_time_hours`, `status` {open, closed, assigned, done, cancelled}
- `created_at`, `deadline`
- `tags/categoría` (ej. chapa, pintura, soldadura)

### Proposal (Bid)
- `id`, `job` (FK → JobOffer), `chapista_profile` (FK)
- `message`, `proposed_price`, `proposed_time_hours`, `status` {pending, accepted, rejected}
- `created_at`

### PortfolioItem
- `chapista_profile` (FK), `title`, `description`, `photos` (separate Photo model), `date`, `tags`

### Photo
- `file_path/url`, `portfolio_item` (FK nullable), `uploaded_at`, `meta`

### Review
- `job` (FK), `from_user` (FK), `to_user` (FK), `rating` (int 1..5), `comment`, `created_at`

### Booking/Work
- `job`, `chapista`, `company`, `agreed_price`, `agreed_time`, `status` (in_progress, finished)
- `started_at`, `finished_at`

### Transaction
- `booking`, `amount`, `status`, `provider_id`, `created_at`

---

## Relaciones Clave y Reglas de Negocio

- **User** tiene `role`; chapista/profile uno-a-uno con user.
- **JobOffer** creada por CompanyProfile; visibilidad pública o solo empresas locales.
- Chapista puede crear múltiples PortfolioItem.
- Empresa recibe múltiples Proposals; al aceptar se crea Booking/Work y se cierra oferta.
- Solo usuarios implicados pueden ver ciertos datos (autorización).

---

## Endpoints Mínimos (REST)

- **Auth**: register / login / logout / JWT (o sesiones Django)
- **Users**: obtener/editar perfil
- **Chapista profile**: crear/editar (portafolio)
- **Company**: crear oferta (CRUD)
- **Offers**: listado (filtros: location, budget, time, tags), detalle
- **Proposals**: crear propuesta para oferta, listar propuestas de una oferta (empresa)
- **Booking**: aceptar propuesta → crear booking, cambiar estado
- **Reviews**: crear review al finalizar
- **Upload**: endpoint seguro para subir fotos (portfolio)

---

## Búsqueda y Filtros (MVP)

- Filtro por ciudad/provincia (usar text fields en Location)
- Más adelante: búsqueda por radio utilizando lat/lng y cálculo Haversine o PostGIS

---

## Requisitos Infra y No Funcionales (MVP)

- Almacenamiento de imágenes: local (MEDIA_ROOT) en MVP; planear migrar a S3
- Autenticación: Django auth + token (DRF) si vas API-first
- Logs y admin: Django admin para gestionar usuarios, ofertas y propuestas
- Tests básicos: flujos críticos (post offer, post proposal, aceptar)
- Seguridad: validar roles y permisos
- Escalabilidad: mantener separación de apps

---

## Prioridad para el MVP (orden de implementación)

1. Modelo User + roles y login/register
2. ChapistaProfile + PortfolioItem + Photo upload
3. CompanyProfile + JobOffer CRUD
4. Proposal model + endpoints para postular
5. Aceptar propuesta → Booking flow
6. Reviews básicas
7. Búsqueda por ubicación y filtros
8. Admin y tests