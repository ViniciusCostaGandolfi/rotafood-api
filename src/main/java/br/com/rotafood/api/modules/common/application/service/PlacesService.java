package br.com.rotafood.api.modules.common.application.service;

import br.com.rotafood.api.modules.common.application.dto.AddressDto;
import br.com.rotafood.api.modules.common.application.mapper.AddressFromExternalApiMapper;
import br.com.rotafood.api.modules.common.domain.entity.Address;
import br.com.rotafood.api.modules.common.domain.repository.AddressRepository;
import br.com.rotafood.api.modules.order.application.dto.BrasilApiResponse;

import com.google.maps.GeoApiContext;
import com.google.maps.GeocodingApi;
import com.google.maps.model.AddressType;
import com.google.maps.model.ComponentFilter;
import com.google.maps.model.GeocodingResult;
import com.google.maps.model.LatLng;

import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.client.RestTemplate;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
@Validated
public class PlacesService {

    private final AddressRepository addressRepository;
    private final GeoApiContext geoApiContext;
    private final RestTemplate restTemplate;
    private final AddressFromExternalApiMapper addressFromExternalApiMapper;

    public PlacesService(AddressRepository addressRepository, GeoApiContext geoApiContext, RestTemplate restTemplate, AddressFromExternalApiMapper addressFromExternalApiMapper) {
        this.addressRepository = addressRepository;
        this.geoApiContext = geoApiContext;
        this.restTemplate = restTemplate;
        this.addressFromExternalApiMapper = addressFromExternalApiMapper;
    }

    public AddressDto findByCep(String cep) {
        if (cep == null || !cep.matches("\\d{8,9}")) {
            throw new IllegalArgumentException("CEP inválido.");
        }
        Optional<Address> addressOptional = addressRepository.findFirstByPostalCode(cep);

        return addressOptional
                .map(AddressDto::new) 
                .orElseGet(() -> fetchFromApis(cep));
    }

    private AddressDto fetchFromApis(String cep) {
        BrasilApiResponse response = restTemplate.getForObject(
                "https://brasilapi.com.br/api/cep/v2/" + cep,
                BrasilApiResponse.class);

        if (response == null) {
            throw new RuntimeException("CEP não encontrado.");
        }

        return addressFromExternalApiMapper.fromBrasilApiResponse(response);
    }


    public List<AddressDto> searchByAddress(String q) {
        List<Address> localResults = addressRepository.findByFormattedAddressContainingIgnoreCase(q);

        if (localResults.size() >= 3) {
            return localResults.stream()
                    .map(AddressDto::new)
                    .toList();
        }

        GeocodingResult[] googleResults;
        try {
            googleResults = GeocodingApi.newRequest(geoApiContext)
                .address(q)
                .language("pt-BR")
                .components(ComponentFilter.country("BR"))
                .await();
        } catch (Exception e) {
            throw new RuntimeException("Erro ao chamar Geocoding API do Google", e);
        }

        List<AddressDto> finalResults = new ArrayList<>();
        for (GeocodingResult result : googleResults) {
            finalResults.add(addressFromExternalApiMapper.fromGeocodingResult(result));
        }
        return finalResults;
    }

    @Transactional
    public AddressDto reverseGeocode(BigDecimal latitude, BigDecimal longitude) {
        try {
            LatLng location = new LatLng(latitude.doubleValue(), longitude.doubleValue());

            GeocodingResult[] results = GeocodingApi.reverseGeocode(geoApiContext, location)
                    .language("pt-BR")
                    .resultType(AddressType.STREET_ADDRESS)
                    .await();

            if (results == null || results.length == 0) {
                throw new Exception("Não foi possível encontrar um endereço de rua para as coordenadas fornecidas.");
            }

            GeocodingResult candidate = results[0];

            return addressFromExternalApiMapper.fromGeocodingResult(candidate);
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException("Erro inesperado durante o geocoding reverso: " + e.getMessage(), e);
        }
    }




}
