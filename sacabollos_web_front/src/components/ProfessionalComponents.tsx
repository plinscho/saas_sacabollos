import { MapPin, Search, Filter, Star, Phone, MessageCircle } from "lucide-react";
import { useState } from 'react';

interface Professional {
	id: string;
	name: string;
	location: string;
	lat: number;
	lng: number;
	type: 'professional' | 'company';
	rating: number;
	specialties: string[];
	phone?: string;
	email?: string;
	description?: string;
	experience?: string;
	priceRange?: string;
}

interface SearchFiltersProps {
	onSearch: (query: string) => void;
	onLocationChange: (location: string) => void;
	onTypeFilter: (type: 'all' | 'professional' | 'company') => void;
	onSpecialtyFilter: (specialty: string) => void;
}

export function SearchFilters({ onSearch, onLocationChange, onTypeFilter, onSpecialtyFilter }: SearchFiltersProps) {
	const [searchQuery, setSearchQuery] = useState('');
	const [location, setLocation] = useState('');

	const specialties = [
		'Sacabollos sin pintura (PDR)',
		'Reparación tradicional',
		'Daños por granizo',
		'Restauración clásicos',
		'Seguros',
		'Servicio móvil'
	];

	return (
		<div className="bg-white p-6 rounded-lg shadow-sm border mb-6">
			<h2 className="text-lg font-semibold mb-4">Buscar Profesionales</h2>

			<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
				{/* Search query */}
				<div className="relative">
					<Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
					<input
						type="text"
						placeholder="Buscar por nombre..."
						className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
						value={searchQuery}
						onChange={(e) => {
							setSearchQuery(e.target.value);
							onSearch(e.target.value);
						}}
					/>
				</div>

				{/* Location */}
				<div className="relative">
					<MapPin className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
					<input
						type="text"
						placeholder="Ciudad, provincia..."
						className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
						value={location}
						onChange={(e) => {
							setLocation(e.target.value);
							onLocationChange(e.target.value);
						}}
					/>
				</div>

				{/* Type filter */}
				<select
					className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
					onChange={(e) => onTypeFilter(e.target.value as 'all' | 'professional' | 'company')}
				>
					<option value="all">Todos</option>
					<option value="professional">Solo Profesionales</option>
					<option value="company">Solo Empresas</option>
				</select>

				{/* Specialty filter */}
				<select
					className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
					onChange={(e) => onSpecialtyFilter(e.target.value)}
				>
					<option value="">Todas las especialidades</option>
					{specialties.map((specialty) => (
						<option key={specialty} value={specialty}>
							{specialty}
						</option>
					))}
				</select>
			</div>
		</div>
	);
}

interface ProfessionalCardProps {
	professional: Professional;
	onContact: (professional: Professional) => void;
	onViewProfile: (professional: Professional) => void;
}

export function ProfessionalCard({ professional, onContact, onViewProfile }: ProfessionalCardProps) {
	return (
		<div className="bg-white rounded-lg shadow-sm border p-6 hover:shadow-md transition-shadow">
			<div className="flex justify-between items-start mb-4">
				<div>
					<h3 className="text-lg font-semibold">{professional.name}</h3>
					<div className="flex items-center gap-2 text-sm text-gray-600">
						<MapPin className="h-4 w-4" />
						{professional.location}
					</div>
					<div className="flex items-center gap-1 mt-1">
						<Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
						<span className="text-sm font-medium">{professional.rating}</span>
						<span className="text-sm text-gray-500">/5</span>
					</div>
				</div>
				<div className={`px-2 py-1 rounded-full text-xs font-medium ${professional.type === 'professional'
						? 'bg-blue-100 text-blue-800'
						: 'bg-red-100 text-red-800'
					}`}>
					{professional.type === 'professional' ? 'Profesional' : 'Empresa'}
				</div>
			</div>

			{professional.description && (
				<p className="text-sm text-gray-600 mb-3">{professional.description}</p>
			)}

			<div className="mb-4">
				<div className="text-xs text-gray-500 mb-2">Especialidades:</div>
				<div className="flex flex-wrap gap-1">
					{professional.specialties.slice(0, 3).map((specialty, idx) => (
						<span key={idx} className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
							{specialty}
						</span>
					))}
					{professional.specialties.length > 3 && (
						<span className="text-xs text-gray-500">+{professional.specialties.length - 3} más</span>
					)}
				</div>
			</div>

			{professional.priceRange && (
				<div className="mb-4">
					<span className="text-sm font-medium text-green-600">{professional.priceRange}</span>
				</div>
			)}

			<div className="flex gap-2 pt-4 border-t">
				<button
					onClick={() => onViewProfile(professional)}
					className="flex-1 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
				>
					Ver Perfil
				</button>
				<button
					onClick={() => onContact(professional)}
					className="flex items-center gap-1 bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-md text-sm font-medium transition-colors"
				>
					<MessageCircle className="h-4 w-4" />
					Contactar
				</button>
				{professional.phone && (
					<a
						href={`tel:${professional.phone}`}
						className="flex items-center gap-1 bg-green-100 hover:bg-green-200 text-green-700 px-3 py-2 rounded-md text-sm font-medium transition-colors"
					>
						<Phone className="h-4 w-4" />
					</a>
				)}
			</div>
		</div>
	);
}