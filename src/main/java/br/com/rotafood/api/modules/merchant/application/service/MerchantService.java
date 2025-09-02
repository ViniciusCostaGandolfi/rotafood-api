package br.com.rotafood.api.modules.merchant.application.service;

import java.time.Instant;
import java.time.LocalTime;
import java.util.List;
import java.util.Objects;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import br.com.rotafood.api.modules.catalog.application.dto.ShiftDto;
import br.com.rotafood.api.modules.catalog.application.service.CatalogService;
import br.com.rotafood.api.modules.catalog.domain.entity.Shift;
import br.com.rotafood.api.modules.common.application.dto.AddressDto;
import br.com.rotafood.api.modules.common.domain.entity.Address;
import br.com.rotafood.api.modules.common.domain.repository.AddressRepository;
import br.com.rotafood.api.modules.merchant.application.dto.FullMerchantDto;
import br.com.rotafood.api.modules.merchant.application.dto.MerchantCreateDto;
import br.com.rotafood.api.modules.merchant.application.dto.MerchantLogisticSettingDto;
import br.com.rotafood.api.modules.merchant.application.dto.MerchantOrderEstimateDto;
import br.com.rotafood.api.modules.merchant.application.dto.MerchantOwnerCreationDto;
import br.com.rotafood.api.modules.merchant.application.dto.OwnerCreateDto;
import br.com.rotafood.api.modules.merchant.domain.entity.Merchant;
import br.com.rotafood.api.modules.merchant.domain.entity.MerchantLogisticSetting;
import br.com.rotafood.api.modules.merchant.domain.entity.MerchantOrderEstimate;
import br.com.rotafood.api.modules.merchant.domain.entity.MerchantUser;
import br.com.rotafood.api.modules.merchant.domain.entity.MerchantUserRole;
import br.com.rotafood.api.modules.merchant.domain.repository.MerchantLogisticSettingRepository;
import br.com.rotafood.api.modules.merchant.domain.repository.MerchantOrderEstimateRepository;
import br.com.rotafood.api.modules.merchant.domain.repository.MerchantRepository;
import br.com.rotafood.api.modules.merchant.domain.repository.MerchantUserRepository;
import br.com.rotafood.api.modules.order.domain.entity.OrderSalesChannel;
import jakarta.persistence.EntityNotFoundException;
import jakarta.transaction.Transactional;

@Service
public class MerchantService {

    @Autowired
    private MerchantRepository merchantRepository;

    @Autowired
    private MerchantUserRepository merchantUserRepository;

    @Autowired
    private AddressRepository addressRepository;

    @Autowired
    private CatalogService catalogService;

    @Autowired
    private MerchantOrderEstimateRepository merchantOrderEstimateRepository;

    @Autowired
    private MerchantLogisticSettingRepository logisticSettingRepository;

    @Transactional
    public MerchantUser createMerchant(MerchantOwnerCreationDto merchantOwnerCreationDto) {
        validateOwnerEmail(merchantOwnerCreationDto.owner().email());

        Address address = createAddress(merchantOwnerCreationDto.merchant().address());
        
        Merchant merchant = createMerchantEntity(merchantOwnerCreationDto.merchant(), address, merchantOwnerCreationDto.owner().email());

        MerchantUser merchantUser = createOwer(merchantOwnerCreationDto.owner(), merchant);

        merchantUser = this.merchantUserRepository.save(merchantUser);

        catalogService.createDefaultCatalogsForMerchant(merchant);

        return merchantUser;
    }

    @Transactional
    public void updateMerchantOpened(UUID merchantId, List<OrderSalesChannel> sources, boolean open) {
        Merchant merchant = merchantRepository.findById(merchantId)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Merchant not found"));

        if (sources.contains(OrderSalesChannel.ROTAFOOD)) {
            Instant timestamp = open
                ? Instant.now()                    
                : Instant.now().minusSeconds(30); 
            merchant.setLastOpenedUtc(timestamp);
            merchantRepository.save(merchant);
        }
    }

    private void validateOwnerEmail(String email) {
        if (merchantUserRepository.existsByEmail(email)) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Email already exists!");
        }
    }

    private Address createAddress(AddressDto addressDto) {
        return addressRepository.save(new Address(addressDto));
    }

    private Merchant createMerchantEntity(MerchantCreateDto merchantDto, Address address, String ownerEmail) {
        Merchant merchant = new Merchant(
            null,
            merchantDto.name(),
            UUID.randomUUID().toString(),
            merchantDto.description(),
            merchantDto.documentType(),
            merchantDto.document(),
            merchantDto.phone(),
            ownerEmail,
            null,
            merchantDto.merchantType(),
            Instant.now(),
            Instant.now(),
            null,
            null,
            null,
            false, 
            address,
            null,
            null,
            null

        );
        return merchantRepository.save(merchant);
    }

    @Transactional
    public Merchant updateMerchant(FullMerchantDto merchantDto) {

        Merchant merchant = merchantRepository.findById(merchantDto.id())
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Merchant not found"));

        String existingOnlineName = merchant.getOnlineName();
        if ((existingOnlineName == null || !existingOnlineName.equals(merchantDto.onlineName())) &&
            merchantRepository.existsByOnlineName(merchantDto.onlineName())) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Online name already in use");
        }
        merchant.setName(merchantDto.name());
        merchant.setOnlineName(merchantDto.onlineName());
        merchant.setPhone(merchantDto.phone());
        merchant.setDescription(merchantDto.description());
        merchant.setImagePath(merchantDto.imagePath());
        merchant.setDocumentType(merchantDto.documentType());
        merchant.setDocument(merchantDto.document());
        merchant.setMerchantType(merchantDto.merchantType());

        if (merchantDto.address() != null) {
            Address currentAddress = merchantDto.address().id() != null ? 
                this.addressRepository.findById(merchantDto.address().id())
                .orElseThrow(() -> new EntityNotFoundException("Endereço não encontrado"))
                : new Address(merchantDto.address());
            currentAddress.updateFromAddressDto(merchantDto.address());
            addressRepository.save(currentAddress);
        }
        
        if (merchantDto.logisticSetting() != null) {
            this.createOrUpdateSettings(merchantDto.logisticSetting(), merchant);
        }

        if (merchantDto.orderEstimate() != null) {
            this.createOrUpdateOrderEstimate(merchantDto.orderEstimate(), merchant);
        }

        if (merchantDto.openingHours() != null) {
            this.updateOpeningHours(merchantDto.openingHours(), merchant);
        }

        return merchantRepository.save(merchant);
    }

    public void createOrUpdateSettings(MerchantLogisticSettingDto settingDto, Merchant merchant) {



        MerchantLogisticSetting setting = merchant.getLogisticSetting() != null
            ? merchant.getLogisticSetting() : new MerchantLogisticSetting();

        setting.setMaxDeliveryRadiusKm(settingDto.maxDeliveryRadiusKm());
        setting.setMinDeliveryFee(settingDto.minDeliveryFee());
        setting.setDeliveryFeePerKm(settingDto.deliveryFeePerKm());
        setting.setFreeDeliveryRadiusKm(settingDto.freeDeliveryRadiusKm());
        setting.setLatitude(settingDto.latitude());
        setting.setLongitude(settingDto.longitude());

        logisticSettingRepository.save(setting);
        merchant.setLogisticSetting(setting);

    }


    public void createOrUpdateOrderEstimate(MerchantOrderEstimateDto estimateDto, Merchant merchant) {
        MerchantOrderEstimate estimate = merchant.getOrderEstimate() != null 
            ?   merchant.getOrderEstimate() : new MerchantOrderEstimate();
  
        estimate.setPickupMinMinutes(estimateDto.pickupMinMinutes());
        estimate.setPickupMaxMinutes(estimateDto.pickupMaxMinutes());
        estimate.setDeliveryMinMinutes(estimateDto.deliveryMinMinutes());
        estimate.setDeliveryMaxMinutes(estimateDto.deliveryMaxMinutes());
        merchantOrderEstimateRepository.save(estimate);
        merchant.setOrderEstimate(estimate);
    }

    private void updateOpeningHours(List<ShiftDto> openingHoursDtos, Merchant merchant) {
    
        List<UUID> incomingIds = openingHoursDtos.stream()
            .map(ShiftDto::id)
            .filter(Objects::nonNull)
            .toList();

        merchant.getOpeningHours().removeIf(shift -> !incomingIds.contains(shift.getId()));

        openingHoursDtos.forEach(dto -> {
                Shift shift = merchant.getOpeningHours().stream()
                    .filter(existing -> existing.getId() != null && existing.getId().equals(dto.id()))
                    .findFirst()
                    .orElseGet(() -> {
                        Shift newShift = new Shift();
                        merchant.addShift(newShift);
                        return newShift;
                    });
                shift.setStartTime(LocalTime.parse(dto.startTime()));
                shift.setEndTime(LocalTime.parse(dto.endTime()));
                shift.setMonday(dto.monday());
                shift.setTuesday(dto.tuesday());
                shift.setWednesday(dto.wednesday());
                shift.setThursday(dto.thursday());
                shift.setFriday(dto.friday());
                shift.setSaturday(dto.saturday());
                shift.setSunday(dto.sunday());
                merchant.addShift(shift);
                });
    }


    private MerchantUser createOwer(OwnerCreateDto ownerDto, Merchant merchant) {
        MerchantUser merchantUser = new MerchantUser();
        merchantUser.setName(ownerDto.name());
        merchantUser.setEmail(ownerDto.email());
        merchantUser.setPassword(ownerDto.password());
        merchantUser.setPhone(ownerDto.phone());
        merchantUser.setRole(MerchantUserRole.OWNER);
        merchantUser.setMerchant(merchant);
        return merchantUserRepository.save(merchantUser);
    }

    public MerchantUser getMerchantUserByEmail(String email) {
        return this.merchantUserRepository.findByEmail(email);
    }

    public boolean existMerchantByOnlineName(String onlineName) {
        return this.merchantRepository.existsByOnlineName(onlineName);
    }

    public Merchant getMerchantById(UUID id) {
        return this.merchantRepository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Merchant not found"));
    }
}
