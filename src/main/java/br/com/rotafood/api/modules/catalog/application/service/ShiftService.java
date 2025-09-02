package br.com.rotafood.api.modules.catalog.application.service;

import br.com.rotafood.api.modules.catalog.application.dto.ShiftDto;
import br.com.rotafood.api.modules.catalog.domain.entity.Item;
import br.com.rotafood.api.modules.catalog.domain.entity.Shift;
import br.com.rotafood.api.modules.merchant.domain.entity.Merchant;
import br.com.rotafood.api.modules.merchant.domain.repository.ShiftRepository;
import jakarta.persistence.EntityNotFoundException;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalTime;
import java.util.List;
import java.util.UUID;

@Service
public class ShiftService {

    @Autowired
    private ShiftRepository shiftRepository;

    @Transactional
    public List<Shift> getShiftsByItem(UUID itemId) {
        return shiftRepository.findByItemId(itemId);
    }

    @Transactional
    public List<Shift> getShiftsByMerchant(UUID merchantId) {
        return shiftRepository.findByMerchantId(merchantId);
    }

    @Transactional
    public Shift updateOrCreate(ShiftDto shiftDto, Item item, Merchant merchant) {
        Shift shift = shiftDto.id() != null
                ? shiftRepository.findById(shiftDto.id())
                  .orElse(new Shift())
                : new Shift();

        shift.setStartTime(LocalTime.parse(shiftDto.startTime()));
        shift.setEndTime(LocalTime.parse(shiftDto.endTime()));
        shift.setMonday(shiftDto.monday());
        shift.setTuesday(shiftDto.tuesday());
        shift.setWednesday(shiftDto.wednesday());
        shift.setThursday(shiftDto.thursday());
        shift.setFriday(shiftDto.friday());
        shift.setSaturday(shiftDto.saturday());
        shift.setSunday(shiftDto.sunday());

        if (item != null) {
            item.addShift(shift);
        }

        if (merchant != null) {
            merchant.addShift(shift);
        }

        return shiftRepository.save(shift); 
    }

    @Transactional
    public void deleteShift(UUID shiftId) {
        Shift shift = shiftRepository.findById(shiftId)
                .orElseThrow(() -> new EntityNotFoundException("Shift não encontrado."));
        shiftRepository.delete(shift);
    }

    @Transactional
    public void deleteShiftsByRelatedEntity(UUID relatedId, String relatedType) {
        switch (relatedType.toLowerCase()) {
            case "item" -> shiftRepository.deleteByItemId(relatedId);
            case "merchant" -> shiftRepository.deleteByMerchantId(relatedId);
            default -> throw new IllegalArgumentException("Tipo de entidade relacionado inválido.");
        }
    }


    @Transactional
    public void deleteAll(List<Shift> shifts) {
        this.shiftRepository.deleteAll(shifts);
    }
}

