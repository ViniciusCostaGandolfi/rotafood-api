package br.com.rotafood.api.modules.catalog.application.service;


import java.util.List;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import br.com.rotafood.api.modules.catalog.application.dto.OptionDto;
import br.com.rotafood.api.modules.catalog.application.dto.ProductDto;
import br.com.rotafood.api.modules.catalog.domain.entity.Option;
import br.com.rotafood.api.modules.catalog.domain.entity.OptionGroup;
import br.com.rotafood.api.modules.catalog.domain.entity.Product;
import br.com.rotafood.api.modules.catalog.domain.entity.Serving;
import br.com.rotafood.api.modules.merchant.domain.entity.Merchant;
import br.com.rotafood.api.modules.merchant.domain.repository.MerchantRepository;
import br.com.rotafood.api.modules.merchant.domain.repository.OptionRepository;
import br.com.rotafood.api.modules.merchant.domain.repository.ProductRepository;
import jakarta.persistence.EntityNotFoundException;
import jakarta.transaction.Transactional;

@Service
public class OptionService {

    @Autowired
    private OptionRepository optionRepository;

    @Autowired
    private ContextModifierService contextModifierService;

    @Autowired
    private ProductRepository productRepository;

    @Autowired
    private MerchantRepository merchantRepository;

    @Transactional
    public Option updateOrCreate(OptionDto optionDto, OptionGroup optionGroup) {
        Option option = optionDto.id() != null
            ? optionRepository.findById(optionDto.id()).orElse(new Option())
            : new Option();

        Product product = this.updateOrCreateProductOption(
            optionDto.product(), 
            optionGroup.getMerchant().getId()
            );

        option.setStatus(optionDto.status());

        option.setIndex(optionDto.index());

        option.setFractions(optionDto.fractions());

        option.setProduct(product);

        if (!optionGroup.getOptions().contains(option)) {
            optionGroup.addOption(option);
        }

        optionRepository.save(option);

        optionDto.contextModifiers().forEach(cm -> {
            var parentOption = cm.parentOptionId() != null ? 
                optionRepository
                    .findById(cm.parentOptionId())
                    .orElseThrow(() -> new EntityNotFoundException("Parent Option não encontrada")) : null;

            this.contextModifierService.updateOrCreate(cm, null, option, parentOption);
        });

        return option;
    }

    @Transactional
    public Product updateOrCreateProductOption(ProductDto productDto, UUID merchantId) {
        Merchant merchant = this.merchantRepository.getReferenceById(merchantId);

        Product product = productDto.id() != null
                ? productRepository.findById(productDto.id())
                        .orElse(new Product())
                : new Product();

        product.setMerchant(merchant);
        product.setName(productDto.name());
        product.setDescription(productDto.description());
        product.setEan(productDto.ean());
        product.setImagePath(productDto.imagePath());
        product.setServing(Serving.NOT_APPLICABLE);
        product.setQuantity(productDto.quantity());
        

        return productRepository.save(product);
    }

    @Transactional
    public void deleteByIdAndMerchantId(UUID optionId, UUID merchantId) {
        Option option = optionRepository.findById(optionId)
            .orElseThrow(() -> new IllegalArgumentException("Option não encontrada."));
    
        optionRepository.delete(option);

    }



    @Transactional
    public void deleteAll(List<Option> options) {
        this.optionRepository.deleteAll(options);
    }
    

}
