import { isMobile, isTablet, isDesktop } from 'react-device-detect';

export const getDeviceType = () => {
    if (isTablet) return 'tablet';
    if (isMobile) return 'mobile';
    return 'desktop';
};

export const canAccessFieldOperations = () => {
    // Saha operasyonu sadece mobilden (veya tablet)
    return isMobile || isTablet;
};

export const canAccessOfficeOperations = () => {
    // Ofis operasyonu sadece desktop
    // User request: "Saha ise !isMobile -> Hata. Ofis ise isMobile -> Hata."
    return isDesktop;
};
