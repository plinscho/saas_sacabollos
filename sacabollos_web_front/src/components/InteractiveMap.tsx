'use client';

import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import { Icon, LatLngBounds } from 'leaflet';
import 'leaflet/dist/leaflet.css';


// Fix Leaflet default markers in Next.js
delete (Icon.Default.prototype as unknown as { _getIconUrl: unknown })._getIconUrl;
Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
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
}

interface InteractiveMapProps {
    professionals: Professional[];
    onProfessionalSelect?: (professional: Professional) => void;
}

// Custom icons for different types
const professionalIcon = new Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

const companyIcon = new Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

function MapUpdater({ professionals }: { professionals: Professional[] }) {
    const map = useMap();

    useEffect(() => {
        if (professionals.length > 0) {
            const bounds = new LatLngBounds(
                professionals.map(p => [p.lat, p.lng])
            );
            map.fitBounds(bounds, { padding: [20, 20] });
        }
    }, [professionals, map]);

    return null;
}

export default function InteractiveMap({ professionals, onProfessionalSelect }: InteractiveMapProps) {
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        setMounted(true);
    }, []);

    if (!mounted) {
        return (
            <div className="h-full w-full bg-gray-100 rounded-lg flex items-center justify-center">
                <div className="text-gray-500">Cargando mapa...</div>
            </div>
        );
    }

    return (
        <MapContainer
            center={[40.4168, -3.7038]} // Madrid center as default
            zoom={6}
            style={{ height: '100%', width: '100%', borderRadius: '0.5rem' }}
            className="z-0"
        >
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            <MapUpdater professionals={professionals} />

            {professionals.map((professional) => (
                <Marker
                    key={professional.id}
                    position={[professional.lat, professional.lng]}
                    icon={professional.type === 'professional' ? professionalIcon : companyIcon}
                    eventHandlers={{
                        click: () => onProfessionalSelect?.(professional)
                    }}
                >
                    <Popup>
                        <div className="p-2 min-w-[200px]">
                            <h3 className="font-semibold text-lg mb-1">{professional.name}</h3>
                            <div className="text-sm text-gray-600 mb-2">
                                <div className="flex items-center gap-1">
                                    <span className={`inline-block w-2 h-2 rounded-full ${professional.type === 'professional' ? 'bg-blue-500' : 'bg-red-500'
                                        }`}></span>
                                    {professional.type === 'professional' ? 'Profesional' : 'Empresa'}
                                </div>
                                <div>📍 {professional.location}</div>
                                <div>⭐ {professional.rating}/5</div>
                            </div>

                            <div className="mb-2">
                                <div className="text-xs text-gray-500 mb-1">Especialidades:</div>
                                <div className="flex flex-wrap gap-1">
                                    {professional.specialties.map((specialty, idx) => (
                                        <span key={idx} className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                                            {specialty}
                                        </span>
                                    ))}
                                </div>
                            </div>

                            <div className="flex gap-2 mt-3">
                                <button
                                    className="bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600"
                                    onClick={() => onProfessionalSelect?.(professional)}
                                >
                                    Ver Perfil
                                </button>
                                {professional.phone && (
                                    <a
                                        href={`tel:${professional.phone}`}
                                        className="bg-green-500 text-white px-3 py-1 rounded text-sm hover:bg-green-600"
                                    >
                                        Llamar
                                    </a>
                                )}
                            </div>
                        </div>
                    </Popup>
                </Marker>
            ))}
        </MapContainer>
    );
}