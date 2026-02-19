import React, { useEffect, useRef, useState } from 'react';
import { Html5QrcodeScanner, Html5Qrcode } from 'html5-qrcode';
import { XMarkIcon } from '@heroicons/react/24/outline';

const BarcodeScanner = ({ onScanSuccess, onScanFailure, onClose }) => {
    const scannerRef = useRef(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Html5QrcodeScanner config
        const config = {
            fps: 10,
            qrbox: { width: 250, height: 250 },
            aspectRatio: 1.0,
            disableFlip: false,
        };

        // Note: We use unique ID for the container
        const html5QrcodeScanner = new Html5QrcodeScanner(
            "reader",
            config,
            /* verbose= */ false
        );

        const successCallback = (decodedText, decodedResult) => {
            // Success!
            console.log(`Scan result: ${decodedText}`, decodedResult);
            // Stop scanning automatically on success if needed, or just callback
            // html5QrcodeScanner.clear(); // We might want to keep scanning or close modal logic handles it
            onScanSuccess(decodedText);
        };

        const errorCallback = (errorMessage) => {
            // Parse error, ignore mostly
            // console.warn(`Scan error: ${errorMessage}`);
            if (onScanFailure) onScanFailure(errorMessage);
        };

        html5QrcodeScanner.render(successCallback, errorCallback);

        // Cleanup
        return () => {
            html5QrcodeScanner.clear().catch(error => {
                console.error("Failed to clear html5QrcodeScanner. ", error);
            });
        };
    }, []);

    return (
        <div className="fixed inset-0 bg-black bg-opacity-90 flex flex-col items-center justify-center z-50 p-4">
            <div className="w-full max-w-sm bg-white rounded-2xl overflow-hidden relative">
                <button
                    onClick={onClose}
                    className="absolute top-2 right-2 z-10 bg-white rounded-full p-1 shadow-md text-gray-800"
                >
                    <XMarkIcon className="w-6 h-6" />
                </button>

                <div className="p-4 bg-gray-900 text-white text-center">
                    <h3 className="font-bold text-lg">Barkod Tara</h3>
                    <p className="text-xs text-gray-400">Kamerayı barkoda tutun</p>
                </div>

                <div id="reader" className="w-full h-auto bg-gray-100"></div>

                {error && (
                    <div className="p-2 bg-red-100 text-red-600 text-xs text-center">
                        {error}
                    </div>
                )}
            </div>
            <button onClick={onClose} className="mt-4 text-white underline">
                Kapat
            </button>
        </div>
    );
};

export default BarcodeScanner;
