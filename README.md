Objetivo MVP:
	Permitir que chapistas autónomos creen perfil y portafolio.
	Permitir que empresas creen ofertas de trabajo (localización, tiempo estimado, presupuesto).
	Permitir que chapistas presenten propuestas (presupuesto / plazo) a ofertas.

Flujo básico: 
	empresa publica oferta → chapistas postulan → empresa acepta → marcar trabajo completado → dejar reseña.
	Búsqueda básica de chapistas/ofertas por localización y filtros.

Apps backend recomendadas (separadas para responsabilidad)
	users: autenticación, roles, datos básicos de usuario (ya presente). models.py
	profiles: perfiles extendidos para chapistas y empresas (si prefieres, integrar en users)
	companies: datos de empresas (siempre que no estén como simple role en users)
	jobs (o offers): ofertas de trabajo (publicadas por empresas)
	proposals (o bids): propuestas de chapistas para una oferta
	portfolios: trabajos y fotos subidas por chapistas
	reviews: valoraciones y comentarios
	locations: ciudades/zonas, o geo-coords (ya presente). models.py
	notifications: notificaciones internas (email/Push más adelante)
	payments (opcional en MVP, o “placeholder”): manejo de pagos/impago/garantías

Modelos recomendados (MVP mínimo; cada modelo = tabla)

User (extiende AbstractUser)
	id, email, username, password, role {chapista, company, admin}
	campos básicos y flags
	archivo: models.py

ChapistaProfile
	user (FK → User, unique)
	display_name, phone, bio, servicios_ofrecidos (tags), precio_hora_estimado, rating_promedio
	is_verified (documentación)
	location (FK → Location o lat/lng)
	disponibilidad (opcional mínimo: boolean / horario)

CompanyProfile
	ser (FK → User)
	company_name, contact_person, phone, address, verified

Location (ya app locations)
	city, province, country, lat, lng, postal_code
	puedes usar solo city/string para MVP, mejorar a geo para búsquedas por radio

JobOffer
	id, company (FK → CompanyProfile), title, description, location (FK → Location o text), budget_min, budget_max, estimated_time_hours, status {open, closed, assigned, done, cancelled}, created_at, deadline
	tags/categoría (ej. chapa, pintura, soldadura)

Proposal (Bid)
	id, job (FK → JobOffer), chapista_profile (FK), message, proposed_price, proposed_time_hours, status {pending, accepted, rejected}, created_at

PortfolioItem
	chapista_profile (FK), title, description, photos (separate Photo model), date, tags

Photo (para portfolio y job)
	file_path/url, portfolio_item (FK nullable), uploaded_at, meta

Review
	job (FK), from_user (FK), to_user (FK), rating (int 1..5), comment, created_at

Booking/Work (una vez aceptada una proposal)
	job, chapista, company, agreed_price, agreed_time, status (in_progress, finished), started_at, finished_at

Transaction (si pago en plataforma)
	booking, amount, status, provider_id, created_at


Relaciones clave y reglas de negocio (básico):

User tiene role; chapista/profile uno-a-uno con user.
JobOffer creada por CompanyProfile; visibilidad pública o solo empresas locales.
Chapista puede crear múltiples PortfolioItem.
Empresa recibe múltiples Proposals; al aceptar se crea Booking/Work y se cierra oferta (status).
Solo usuarios implicados pueden ver ciertos datos (autorización).

Endpoints mínimos (REST)

Auth: register / login / logout / JWT (o sesiones Django)
Users: obtener/editar perfil
Chapista profile: crear/editar (portafolio)
Company: crear oferta (CRUD)
Offers: listado (filtros: location, budget, time, tags), detalle
Proposals: crear propuesta para oferta, listar propuestas de una oferta (empresa)
Booking: aceptar propuesta → crear booking, cambiar estado
Reviews: crear review al finalizar
Upload: endpoint seguro para subir fotos (portfolio) — almacenamiento local en MVP


Búsqueda y filtros (MVP)
Filtro por ciudad/provincia para empezar (usar text fields en Location).
Más adelante: búsqueda por radio utilizando lat/lng y calculo Haversine o PostGIS.

Requisitos infra y no funcionales (MVP)
Almacenamiento de imágenes: local (MEDIA_ROOT) en MVP; planear migrar a S3.
Autenticación: Django auth + token (DRF) si vas API-first.
Logs y admin: Django admin para gestionar usuarios, ofertas y propuestas.
Tests básicos: flujos críticos (post offer, post proposal, aceptar).
Seguridad: validar roles y permisos (solo company puede aceptar propuestas, solo autor puede editar portafolio).
Escalabilidad: mantener separación de apps para separar responsabilidades.


Prioridad para el MVP (orden de implementación)
Modelo User + roles y login/register.
ChapistaProfile + PortfolioItem + Photo upload.
CompanyProfile + JobOffer CRUD.
Proposal model + endpoints para postular.
Aceptar propuesta → Booking flow.
Reviews básicas.
Búsqueda por ubicación y filtros.
Admin y tests.