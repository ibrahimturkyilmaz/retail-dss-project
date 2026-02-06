import { useQuery } from '@tanstack/react-query';
import axiosClient from '../api/axios';

const fetchStores = async () => {
    const { data } = await axiosClient.get('/stores');
    return data;
};

export const useStores = () => {
    return useQuery({
        queryKey: ['stores'],
        queryFn: fetchStores,
        staleTime: 1000 * 60 * 5, // 5 dakika boyunca taze kabul et
        refetchOnWindowFocus: false,
    });
};
