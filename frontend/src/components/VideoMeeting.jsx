import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';

const VideoMeeting = ({ roomName = "Genel-Toplantı" }) => {
    const { user } = useAuth();
    const [loading, setLoading] = useState(true);
    const jitsiContainerId = "jitsi-container-id";

    useEffect(() => {
        // Jitsi kütüphanesini dinamik olarak yükle
        const script = document.createElement("script");
        script.src = "https://meet.jit.si/external_api.js";
        script.async = true;
        script.onload = () => initJitsi();
        document.body.appendChild(script);

        return () => {
            document.body.removeChild(script);
        };
    }, []);

    const initJitsi = () => {
        setLoading(false);
        if (!window.JitsiMeetExternalAPI) return;

        const domain = "meet.jit.si";
        const options = {
            roomName: `RetailDSS-${roomName}`,
            width: "100%",
            height: "100%",
            parentNode: document.getElementById(jitsiContainerId),
            userInfo: {
                displayName: user?.email || "Misafir Kullanıcı",
                email: user?.email
            },
            configOverwrite: {
                startWithAudioMuted: true,
                startWithVideoMuted: false
            },
            interfaceConfigOverwrite: {
                SHOW_JITSI_WATERMARK: false,
                SHOW_WATERMARK_FOR_GUESTS: false,
                TOOLBAR_BUTTONS: [
                    'microphone', 'camera', 'closedcaptions', 'desktop', 'fullscreen',
                    'fodeviceselection', 'hangup', 'profile', 'chat', 'recording',
                    'livestreaming', 'etherpad', 'sharedvideo', 'settings', 'raisehand',
                    'videoquality', 'filmstrip', 'invite', 'feedback', 'stats', 'shortcuts',
                    'tileview', 'videobackgroundblur', 'download', 'help', 'mute-everyone',
                    'security'
                ],
            }
        };

        const api = new window.JitsiMeetExternalAPI(domain, options);
    };

    return (
        <div className="flex flex-col h-full w-full bg-gray-900 rounded-2xl overflow-hidden shadow-2xl border border-gray-700">
            {loading && (
                <div className="flex items-center justify-center h-full text-white">
                    <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-emerald-500"></div>
                </div>
            )}
            <div id={jitsiContainerId} className="w-full h-full" />
        </div>
    );
};

export default VideoMeeting;
