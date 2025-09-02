package br.com.rotafood.api.modules.catalog.application.service;

import java.util.Date;
import java.util.List;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import br.com.rotafood.api.modules.catalog.application.dto.CatalogDto;
import br.com.rotafood.api.modules.catalog.domain.entity.AvailabilityStatus;
import br.com.rotafood.api.modules.catalog.domain.entity.Catalog;
import br.com.rotafood.api.modules.catalog.domain.entity.CatalogContext;
import br.com.rotafood.api.modules.merchant.domain.entity.Merchant;
import br.com.rotafood.api.modules.merchant.domain.repository.CatalogRepository;
import br.com.rotafood.api.modules.merchant.domain.repository.MerchantRepository;
import jakarta.persistence.EntityNotFoundException;

@Service
public class CatalogService {

    @Autowired private CatalogRepository catalogRepository;
    @Autowired private MerchantRepository merchantRepository;

    public List<CatalogDto> getAllByMerchantId(UUID merchantId) {
        return catalogRepository.findAllByMerchantId(merchantId)
                .stream()
                .map(CatalogDto::new)
                .toList();
    }

    @Transactional
    public Catalog getByIdAndMerchantId(UUID catalogId, UUID merchantId) {
        return catalogRepository.findByIdAndMerchantId(catalogId, merchantId);
    }

    @Transactional
    public Catalog updateOrCreate(CatalogDto catalogDto, UUID merchantId) {
        Merchant merchant = merchantRepository.findById(merchantId)
                .orElseThrow(() -> new EntityNotFoundException("Merchant não encontrado."));

        Catalog catalog;

        if (catalogDto.id() != null) {
            catalog = catalogRepository.findByIdAndMerchantId(catalogDto.id(), merchantId);
            if (catalog == null) {
                throw new EntityNotFoundException("Catálogo não encontrado.");
            }
            catalog.setModifiedAt(new Date());
            catalog.setStatus(catalogDto.status());
            catalog.setCatalogContext(catalogDto.catalogContext());
        } else {
            catalog = new Catalog();
            catalog.setModifiedAt(new Date());
            catalog.setStatus(catalogDto.status());
            catalog.setCatalogContext(catalogDto.catalogContext());
            catalog.setMerchant(merchant);
            catalog.setIFoodCatalogId(catalogDto.iFoodCatalofId());
        }

        catalog = catalogRepository.save(catalog);

        return catalog;
    }

    @Transactional
    public void createDefaultCatalogsForMerchant(Merchant merchant) {
        List<CatalogDto> defaultCatalogs = List.of(
            new CatalogDto(null, new Date(), AvailabilityStatus.AVAILIABLE, CatalogContext.TABLE, null),
                new CatalogDto(null, new Date(), AvailabilityStatus.AVAILIABLE, CatalogContext.DELIVERY, null),
                new CatalogDto(null, new Date(), AvailabilityStatus.AVAILIABLE, CatalogContext.IFOOD, null)
        );

        defaultCatalogs.forEach(catalogDto -> updateOrCreate(catalogDto, merchant.getId()));
    }
}
