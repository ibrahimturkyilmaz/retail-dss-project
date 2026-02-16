import React from 'react';
import { ArrowPathIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline';

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null, errorInfo: null };
    }

    static getDerivedStateFromError(error) {
        // Update state so the next render will show the fallback UI.
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        // You can also log the error to an error reporting service
        console.error("Uncaught error:", error, errorInfo);
        this.setState({ error, errorInfo });
    }

    handleReload = () => {
        window.location.reload();
    };

    render() {
        if (this.state.hasError) {
            return (
                <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
                    <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 text-center border border-slate-100">
                        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-red-100 mb-6">
                            <ExclamationTriangleIcon className="w-8 h-8 text-red-600" />
                        </div>

                        <h1 className="text-2xl font-bold text-slate-900 mb-2">
                            Beklenmedik Bir Hata Oluştu
                        </h1>

                        <p className="text-slate-500 mb-8 leading-relaxed">
                            Üzgünüz, bir şeyler ters gitti. Bu durum loglandı ve teknik ekibimiz inceliyor.
                        </p>

                        <div className="bg-red-50 rounded-lg p-4 mb-8 text-left overflow-auto max-h-32 text-xs font-mono text-red-800 border border-red-100">
                            {this.state.error && this.state.error.toString()}
                        </div>

                        <button
                            onClick={this.handleReload}
                            className="w-full inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-xl text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all shadow-lg shadow-indigo-200"
                        >
                            <ArrowPathIcon className="w-5 h-5 mr-2" />
                            Sayfayı Yenile
                        </button>

                        <p className="mt-6 text-xs text-slate-400">
                            Hata Kodu: ERR_CLIENT_RENDER
                        </p>
                    </div>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;
