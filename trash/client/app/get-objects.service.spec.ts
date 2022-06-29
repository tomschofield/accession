import { TestBed, inject } from '@angular/core/testing';

import { GetObjectsService } from './get-objects.service';

describe('GetObjectsService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [GetObjectsService]
    });
  });

  it('should ...', inject([GetObjectsService], (service: GetObjectsService) => {
    expect(service).toBeTruthy();
  }));
});
