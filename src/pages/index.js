import dynamic from 'next/dynamic';

// Dynamically import FurnitureConfigurator with SSR disabled
const FurnitureConfigurator = dynamic(
  () => import('@/components/ui/furniture-configurator'),
  { ssr: false }
);

export default function Home() {
  return (
    <div className="min-h-screen">
      <FurnitureConfigurator />
    </div>
  );
}