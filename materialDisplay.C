
void materialDisplay(TString filename,Bool_t checkoverlaps=kFALSE,TString label="geom-test.root" )
{
  
  Int_t PriKolor[] = {  2,  3,  4,  5,  6,  7,  8, 9, 28, 30, 38, 40, 41, 42, 46 };
  Int_t PriIndex = 0;
  std::map<TString,Int_t> Kolor;
  Kolor["Steel"] = kGray;
  Kolor["Copper"] = kYellow;
  Kolor["Aluminum"] = kRed;
  Kolor["FR4"] = kGreen;
  Kolor["LAr"] = kBlue;
  Kolor["PVT"] = kViolet;
  Kolor["Kapton"] = kBlack;
  Kolor["Rock"] = kOrange+3;

  TGeoManager *geo2 = new TGeoManager("geo2","test");
  geo2->Import(filename);
  geo2->SetVisLevel(20);
  TGeoVolume *volume = NULL;
  TObjArray *volumes = geo2->GetListOfVolumes();
  Int_t nvolumes = volumes->GetEntries();
  for ( int i = 0; i < nvolumes; i++ )
  {
    volume = (TGeoVolume*)volumes->At(i);
    volume->SetVisContainers(kTRUE);

    if (TString(volume->GetMaterial()->GetName()).Contains("Air")) volume->SetInvisible();
    if (TString(volume->GetMaterial()->GetName()).Contains("LAr")) volume->SetTransparency(80);
 
    Int_t daughters = volume->GetNdaughters();
    //cout << endl;
		cout << volume->GetName() << endl;
    volume->SetLineColor(Kolor[volume->GetMaterial()->GetName()]);
    if (TString(volume->GetName()).Contains("Connector")) volume->SetLineColor(kBlack);

  }

  geo2->GetTopVolume()->Draw("ogl");
}
