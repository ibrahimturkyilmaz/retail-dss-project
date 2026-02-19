import React from 'react';
import { useTime } from '../../context/TimeContext';

const TimeTravelWidget = () => {
    const { virtualTime, jumpTime, resetTime, canZReport } = useTime();

    // Format time: HH:mm
    const formattedTime = virtualTime.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });

    return (
        <div style={{
            position: 'fixed',
            bottom: '20px',
            right: '20px',
            backgroundColor: '#1e293b',
            color: 'white',
            padding: '10px 15px',
            borderRadius: '8px',
            boxShadow: '0 4px 6px rgba(0,0,0,0.3)',
            zIndex: 9999,
            display: 'flex',
            flexDirection: 'column',
            gap: '8px',
            border: canZReport ? '2px solid #22c55e' : '2px solid #64748b'
        }}>
            <div style={{ fontWeight: 'bold', fontSize: '14px', textAlign: 'center' }}>
                ⏰ Sanal Saat: {formattedTime}
            </div>

            <div style={{ display: 'flex', gap: '5px' }}>
                <button
                    onClick={() => jumpTime(1)}
                    style={{ padding: '4px 8px', backgroundColor: '#3b82f6', border: 'none', borderRadius: '4px', cursor: 'pointer', color: 'white' }}
                >
                    +1 Saat
                </button>
                <button
                    onClick={() => jumpTime(4)}
                    style={{ padding: '4px 8px', backgroundColor: '#8b5cf6', border: 'none', borderRadius: '4px', cursor: 'pointer', color: 'white' }}
                >
                    +4 Saat
                </button>
            </div>
            <button
                onClick={resetTime}
                style={{ padding: '4px 8px', backgroundColor: '#ef4444', border: 'none', borderRadius: '4px', cursor: 'pointer', color: 'white', fontSize: '12px' }}
            >
                Sıfırla
            </button>

            {canZReport && (
                <div style={{ fontSize: '10px', color: '#22c55e', textAlign: 'center' }}>
                    ✅ Kapanış Vakti
                </div>
            )}
        </div>
    );
};

export default TimeTravelWidget;
