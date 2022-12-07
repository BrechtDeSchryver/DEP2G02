from connectie import get_database

pg_engine = get_database()

def insert_score_into_kmo(kmo_id,score):
    args = (score,kmo_id)
    pg_engine.execute('UPDATE kmo SET score = %s WHERE \"ondernemingsNummer\" = %s',args)

def insert_score_into_sector(sector_name,score):
    args = (score,sector_name)
    pg_engine.execute('UPDATE sector SET score = %s WHERE name = %s',args)

def main():
    teller = 0
    res = pg_engine.execute('SELECT score,discriminator,\"forain_ID\" FROM score').all()
    vorig_kmo_id = res[0][2]
    score = 0
    for kmo in res:
        print(f'{round(teller/len(res),4)*100}%')
        domainscore,discr,kmo_id = float(kmo[0]),int(kmo[1]),kmo[2]# discr == 0 -> kmo, discr == 1 -> sector
        if not vorig_kmo_id == kmo_id:
            score*=1/3# score is alle domeinscores opgeteld en 1/3 van die som
            insert_score_into_kmo(kmo_id,score) if discr == 0 else insert_score_into_sector(kmo_id,score)# insert in oftewel sector of kmo door discr parameter
            print(f'({kmo_id}) : Score {score}')
            score=0
        score+=domainscore

        vorig_kmo_id = kmo_id
        teller+=1

    print('Klaar let\'s go')

# main()
