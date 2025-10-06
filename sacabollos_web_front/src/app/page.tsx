'use client';

import { useState } from 'react';
import dynamic from 'next/dynamic';
import { SearchFilters, ProfessionalCard } from '@/components/ProfessionalComponents';
import { MapPin, Users, Star, Zap } from 'lucide-react';

const InteractiveMap = dynamic(() => import('@/components/InteractiveMap'), {
  ssr: false,
  loading: () => (
    <div className="h-full w-full bg-gray-100 rounded-lg flex items-center justify-center">
      <div className="text-gray-500">Cargando mapa...</div>
    </div>
  )
});

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

const mockProfessionals: Professional[] = [
  {
    id: '1',
    name: 'Carlos Rodríguez',
    location: 'Madrid, España',
    lat: 40.4168,
    lng: -3.7038,
    type: 'professional',
    rating: 4.8,
    specialties: ['Sacabollos sin pintura (PDR)', 'Servicio móvil'],
    phone: '+34 600 123 456',
    email: 'carlos@example.com',
    description: '15 años de experiencia en reparación de abollones sin pintura.',
    priceRange: '50-150€ por trabajo'
  }
];

export default function Home() {
  const [professionals] = useState<Professional[]>(mockProfessionals);
  const [filteredProfessionals, setFilteredProfessionals] = useState<Professional[]>(mockProfessionals);
  const [selectedProfessional, setSelectedProfessional] = useState<Professional | null>(null);
  const [viewMode, setViewMode] = useState<'map' | 'list'>('map');

  const handleSearch = (query: string) => {
    const filtered = professionals.filter(p => 
      p.name.toLowerCase().includes(query.toLowerCase())
    );
    setFilteredProfessionals(filtered);
  };

  const handleLocationChange = (location: string) => {
    const filtered = professionals.filter(p => 
      p.location.toLowerCase().includes(location.toLowerCase())
    );
    setFilteredProfessionals(filtered);
  };

  const handleTypeFilter = (type: 'all' | 'professional' | 'company') => {
    if (type === 'all') {
      setFilteredProfessionals(professionals);
    } else {
      const filtered = professionals.filter(p => p.type === type);
      setFilteredProfessionals(filtered);
    }
  };

  const handleSpecialtyFilter = (specialty: string) => {
    if (!specialty) {
      setFilteredProfessionals(professionals);
    } else {
      const filtered = professionals.filter(p => 
        p.specialties.includes(specialty)
      );
      setFilteredProfessionals(filtered);
    }
  };

  const handleContact = (professional: Professional) => {
    alert(`Contactando con ${professional.name}`);
  };

  const handleViewProfile = (professional: Professional) => {
    setSelectedProfessional(professional);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">SacaBollos.eu</h1>
              <p className="text-sm text-gray-600">Conectamos profesionales de reparación de abollones</p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setViewMode('map')}
                className={`px-4 py-2 rounded-md text-sm font-medium ${
                  viewMode === 'map' 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <MapPin className="inline h-4 w-4 mr-1" />
                Mapa
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`px-4 py-2 rounded-md text-sm font-medium ${
                  viewMode === 'list' 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <Users className="inline h-4 w-4 mr-1" />
                Lista
              </button>
            </div>
          </div>
        </div>
      </header>

      <section className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-4xl font-bold mb-4">
              Encuentra el Mejor Profesional de Sacabollos
            </h2>
            <p className="text-xl mb-8 text-blue-100">
              La plataforma europea para conectar profesionales y empresas
            </p>
          </div>
        </div>
      </section>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <SearchFilters
          onSearch={handleSearch}
          onLocationChange={handleLocationChange}
          onTypeFilter={handleTypeFilter}
          onSpecialtyFilter={handleSpecialtyFilter}
        />

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            {viewMode === 'map' ? (
              <div className="h-[600px] rounded-lg overflow-hidden">
                <InteractiveMap
                  professionals={filteredProfessionals}
                  onProfessionalSelect={handleViewProfile}
                />
              </div>
            ) : (
              <div className="space-y-4 max-h-[600px] overflow-y-auto">
                {filteredProfessionals.map((professional) => (
                  <ProfessionalCard
                    key={professional.id}
                    professional={professional}
                    onContact={handleContact}
                    onViewProfile={handleViewProfile}
                  />
                ))}
              </div>
            )}
          </div>

          <div className="space-y-6">
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <h3 className="text-lg font-semibold mb-4">MVP Demo</h3>
              <p className="text-sm text-gray-600">
                Esta es una demostración del concepto. Mejora significativa sobre dentrepair.com 
                con mapa interactivo, filtros avanzados y mejor UX.
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
