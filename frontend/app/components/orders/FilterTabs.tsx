'use client';

interface FilterTabsProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

const tabs = [
  { id: 'all', label: 'All' },
  { id: 'incomplete', label: 'Incomplete' },
  { id: 'overdue', label: 'Overdue' },
  { id: 'ongoing', label: 'Ongoing' },
  { id: 'finished', label: 'Finished' },
];

export default function FilterTabs({ activeTab, onTabChange }: FilterTabsProps) {
  return (
    <div className="flex gap-1 border-b border-gray-200 mb-4">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onTabChange(tab.id)}
          className={`px-4 py-2 text-sm font-medium transition-colors relative ${
            activeTab === tab.id
              ? 'text-gray-800'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          {tab.label}
          {activeTab === tab.id && (
            <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gray-800"></div>
          )}
        </button>
      ))}
    </div>
  );
}
