import { clsx } from 'clsx';

export default function Skeleton({ className }) {
    return (
        <div
            className={clsx(
                "bg-gray-200 animate-pulse rounded-lg",
                className
            )}
        />
    );
}

export function HomeSkeleton() {
    return (
        <div className="p-6 pt-12 space-y-6">
            {/* Header Skeleton */}
            <div className="flex justify-between items-center">
                <div className="space-y-2">
                    <Skeleton className="w-20 h-4" />
                    <Skeleton className="w-40 h-8" />
                </div>
                <Skeleton className="w-10 h-10 rounded-full" />
            </div>

            {/* Hero Skeleton */}
            <Skeleton className="w-full h-48 rounded-3xl" />

            {/* Categories Skeleton */}
            <div className="flex gap-4 overflow-hidden">
                {[...Array(4)].map((_, i) => (
                    <div key={i} className="flex flex-col items-center gap-2">
                        <Skeleton className="w-[72px] h-[72px] rounded-full" />
                        <Skeleton className="w-12 h-3" />
                    </div>
                ))}
            </div>

            {/* Recommended Skeleton */}
            <div className="grid grid-cols-2 gap-4">
                {[...Array(4)].map((_, i) => (
                    <div key={i} className="space-y-2">
                        <Skeleton className="w-full aspect-square rounded-2xl" />
                        <Skeleton className="w-3/4 h-4" />
                        <Skeleton className="w-1/2 h-4" />
                    </div>
                ))}
            </div>
        </div>
    );
}
