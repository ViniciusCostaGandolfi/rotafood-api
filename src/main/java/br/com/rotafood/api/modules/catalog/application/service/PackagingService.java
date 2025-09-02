package br.com.rotafood.api.modules.catalog.application.service;

import java.util.List;
import java.util.UUID;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import br.com.rotafood.api.modules.catalog.application.dto.PackagingDto;
import br.com.rotafood.api.modules.catalog.domain.entity.Packaging;
import br.com.rotafood.api.modules.merchant.domain.entity.Merchant;
import br.com.rotafood.api.modules.merchant.domain.repository.MerchantRepository;
import br.com.rotafood.api.modules.merchant.domain.repository.PackagingRepository;
import jakarta.persistence.EntityNotFoundException;

@Service
public class PackagingService {

    private final PackagingRepository packagingRepository;
    private final MerchantRepository merchantRepository;

    public PackagingService(PackagingRepository packagingRepository, MerchantRepository merchantRepository) {
        this.packagingRepository = packagingRepository;
        this.merchantRepository = merchantRepository;
    }

    public List<PackagingDto> getAllByMerchantId(UUID merchantId) {
        return packagingRepository.findByMerchantId(merchantId)
                .stream()
                .map(PackagingDto::new).toList();
    }

    @Transactional
    public Packaging getByIdAndMerchantId(UUID packagingId, UUID merchantId) {
        return packagingRepository.findByIdAndMerchantId(packagingId, merchantId)
                .orElseThrow(() -> new EntityNotFoundException("Packaging not found."));
    }

    @Transactional
    public Packaging updateOrCreate(PackagingDto packagingDto, UUID merchantId) {
        Merchant merchant = merchantRepository.findById(merchantId)
                .orElseThrow(() -> new EntityNotFoundException("Merchant not found."));

        Packaging packaging = packagingDto.id() != null ? 
            packagingRepository.findByIdAndMerchantId(packagingDto.id(), merchantId).orElse(new Packaging()) : new Packaging();
        
        packaging.setName(packagingDto.name());
        packaging.setImagePath(packagingDto.imagePath());
        packaging.setLenghtCm(packagingDto.lenghtCm());
        packaging.setWidthCm(packagingDto.widthCm());
        packaging.setThicknessCm(packagingDto.thicknessCm());
        packaging.setVolumeMl(packagingDto.volumeMl());

        packaging.setMerchant(merchant);

        return packagingRepository.save(packaging);
    }
}